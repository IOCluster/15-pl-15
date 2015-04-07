from argparse import ArgumentParser, Namespace
import copy
import random
import sys
import time
import threading
import socket
import signal
from time import strftime
from iocluster import messages
from iocluster.master.component import components, backup_servers, CommunicationServer
from iocluster.master.problem import problems, Problem
from iocluster.util import connections_manager, connect
import iocluster.util as Utilities

argfix = {
	"-port": "--port",
	"-backup": "--backup",
}

args = [(x if not x in argfix else argfix[x]) for x in sys.argv[1:]]
parser = ArgumentParser(prog=sys.argv[0], description="Master server")
parser.add_argument('--primary_address', '-pa', type=str, default="", help="primary communication server's IPv4/6 address or host name")
parser.add_argument('--primary_port', '-pp', type=int, default=2121, help="primary communication server's port")
parser.add_argument('--port', '-p', type=int, default=2121, help="port to listen on")
parser.add_argument('--backup', '-b', action="store_true", help="are we a backup server?")
parser.add_argument('--timeout', '-t', type=int, default=5, help="component timeout (s)")
args = parser.parse_args(args)

config = Namespace()
config.parent_address = None
config.parent_port = None
config.child_address = None
config.child_port = None
config.child_id = None
config.is_backup = args.backup
config.timeout = args.timeout

# The important
# information that are synchronized are the existing CN and TM and their current activities and the data of
# tasks, partial problems, partial solutions and final solutions. Each backup server connects first with the
# main CS but if it is not the first backup server it registers with the current last backup server. In that way,
# each backup server needs to store only one set of data to be synchronized. The current information is
# sent to the backup CS when it registers with the CS of a higher level and is updated after each

# [Register or data message message Received || Inactive component removed
# => Add information to synchronization queue and update internal information

def registerTMCN(conn, msg):
	id = components.add(msg)
	print("-> Register :: #{id:d} Type: {type:s}".format(type=msg.Type, id=id))
	response = messages.RegisterResponse(id, config.timeout, components.getBackupServersList())
	conn.send(response)

	backup_msg = copy.deepcopy(msg)
	backup_msg.Id = id
	backup_servers.registerQueueAppend(backup_msg)

def registerBCS(conn, msg):
	peer = conn.socket.getpeername()
	# Current main CS decides component id, if msg.Id exists -> components.add preserves it
	id = components.add(msg, (peer[0], peer[1]))
	# Current server has no backups
	if config.child_address == None and config.child_port == None:
		print("-> Register BCS :: #{id:d}".format(id=id))
		config.child_address = peer[0]
		config.child_port = peer[1]
		config.child_id = id
		response = messages.RegisterResponse(id, config.timeout, [])
		conn.send(response)
		# Send accumulated register messages queue
		for registerMsg in backup_servers.getRegisterMessages():
			conn.send(registerMsg)
	# Forward BCS to first backup server
	else:
		print("-> Send register BCS downstream :: #{id:d}".format(id=msg.Id))
		backups = [{
			"address": config.child_address,
			"port": config.child_port
		}]
		response = messages.RegisterResponse(msg.Id, config.timeout, backups)
		conn.send(response)

def deregisterBCS(conn, msg):
	print("-> Deregister BCS :: #{id:d}".format(id=msg.Id))
	component = components.get(msg.Id)
	component.dead = True
	if config.is_backup:
		# Notify upstream server about deregistering
		backup_msg = copy.deepcopy(msg)
		backup_servers.parentQueueAppend(backup_msg)

def messageRegister(conn, msg):
	if not msg.Type == "CommunicationServer":
		registerTMCN(conn, msg)
	else:
		registerBCS(conn, msg) if not msg.Deregister else deregisterBCS(conn, msg)

def messageStatus(conn, msg):
	component = components.get(msg.Id)
	assert component != None, "component id not registered"
	assert not component.dead, "component already dead"
	print("-> Status :: #{id:d} ({type:s})".format(type=component.type, id=component.id))
	component.touch()
	component.parseStatus(msg)
	component.sendMessages(conn)

def messageSolveRequest(conn, msg):
	id = problems.add(msg)
	print("-> AddProblem :: #{id:d} Type: {type:s} Timeout: {timeout:d}".format(type=msg.ProblemType, timeout=msg.SolvingTimeout, id=id))
	response = messages.SolveRequestResponse(id)
	conn.send(response)

	backup_msg = copy.deepcopy(msg)
	backup_msg.Id = id
	backup_servers.backupQueueAppend(backup_msg)

def messageSolutionRequest(conn, msg):
	assert msg.Id < len(problems.list), "problem id not registered"
	problem = problems.list[msg.Id]
	print("-> SolutionRequest :: #{id:d} Type: {type:s}".format(id=msg.Id, type=problem.getComputationType()))
	response = problem.getSolutionRequestMessage()
	conn.send(response)

def messageSolvePartialProblems(conn, msg):
	assert msg.Id < len(problems.list), "problem id not registered"
	print("-> SolvePartialProblems :: #{id:d} Type: {type:s} PartialProblems: {count:d}".format(type=msg.ProblemType, id=msg.Id, count=len(msg.PartialProblems)))
	problem = problems.list[msg.Id]
	problem.updateWithDivide(msg)

	backup_msg = copy.deepcopy(msg)
	backup_servers.backupQueueAppend(backup_msg)

def messageSolutions(conn, msg):
	problem = problems.list[msg.Id]
	# Received partial solution from CN
	if problem.status == Problem.Divided:
		print("-> Solutions :: #{id:d} Type: {type:s}".format(type=msg.ProblemType, id=msg.Id))
		for solution in msg.Solutions:
			print("--- Solution :: #{id:d} Type: {type:s} Time: {time:d} Timeout: {timeout:}".format(type=solution.Type, time=solution.ComputationsTime, id=solution.TaskId, timeout=solution.TimeoutOccured))
	# Received final merged solution from TM 
	elif problem.status == Problem.Computed:
		print("-> Merged Solutions :: #{id:d} Type: {type:s}".format(type=msg.ProblemType, id=msg.Id))
	problem.updateWithSolutions(msg)

	backup_msg = copy.deepcopy(msg)
	backup_servers.backupQueueAppend(backup_msg)

def parseMessages(conn):
	# Read all messages from client separated by 0x17 until EOC (write stream closed)
	for msg in conn:
		# CS
		if type(msg) == messages.Register:
			messageRegister(conn, msg)
		elif type(msg) == messages.Status:
			messageStatus(conn, msg)
		elif type(msg) == messages.SolveRequest:
			messageSolveRequest(conn, msg)
		elif type(msg) == messages.SolutionRequest:
			messageSolutionRequest(conn, msg)
		elif type(msg) == messages.SolvePartialProblems:
			messageSolvePartialProblems(conn, msg)
		elif type(msg) == messages.Solutions:
			messageSolutions(conn, msg)
		else:
			print("? {:s}".format(str(msg)))

def handleConnection(conn):
	print("{time:s} Connection from {server:s}:{port:d}".format(time=strftime("%H:%M:%S"), server=conn.socket.getpeername()[0], port=conn.socket.getpeername()[1]))
	try:
		parseMessages(conn)
	except AssertionError as e:
		print("Assertion error: {0}".format(e))
	finally:
		# Close connection
		conn.socket.shutdown(socket.SHUT_WR)
		conn.socket.close()
		connections_manager.remove(conn)

def removeInactiveBackup():
	if config.child_id != None:
		component = components.get(config.child_id)
		if not component.isAlive(2 * config.timeout * 1000):
			config.child_id = None
			config.child_address = None
			config.child_port = None

			deregister_msg = copy.deepcopy(component.registerMessage)
			deregister_msg.Id = component.id
			deregister_msg.Deregister = True
			if config.is_backup:
				backup_servers.parentQueueAppend(parent_msg)
			else:
				backup_servers.registerQueueAppend(backup_msg)

def removeInactiveComponents():
	removeInactiveBackup()
	if config.is_backup: return
	for component in components.active():
		# Wait twice the timeout, as nodes are sending state each timeout seconds
		# Don't check CSs, as their state is updated only for the parent in backups list
		if not component.isAlive(2 * config.timeout * 1000) and component.type != "CommunicationServer":
			# Release all problems or tasks assigned to that component
			problems.release(component.id)
			print("Removing inactive component: #{:d} ({:s})".format(component.id, type(component).__name__))

			# Backup message: remove component
			backup_msg = copy.deepcopy(component.registerMessage)
			backup_msg.Id = component.id
			backup_msg.Deregister = True
			backup_servers.registerQueueAppend(backup_msg)

signal.signal(signal.SIGINT, lambda: connections_manager.closeAndExit())

def runServer():
	# Open server socket
	print("Starting server on port {port:d} with timeout {timeout:d}".format(port=args.port, timeout=config.timeout))
	server = socket.socket(socket.AF_INET6)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	while True:
		try:
			server.bind(("::", args.port))
			break
		except:
			print("Trying to bind...")
			time.sleep(1)
	server.listen(50)

	# Main Loop: Listen for incoming connections
	while True:
		try:
			s, addr = server.accept()
		except:
			break
		removeInactiveComponents()
		conn = messages.Connection(s, timeout=config.timeout)
		connections_manager.add(conn)
		threading.Thread(target=handleConnection, args=(conn,)).start()

# Backup server functions

def parseMessageBCS(msg):
	# Forward messages
	if type(msg) == messages.Register: backup_servers.backupQueueAppend(copy.deepcopy(msg))
	else: backup_servers.registerQueueAppend(copy.deepcopy(msg))
	# Parse
	if type(msg) == messages.Register:
		if not msg.Deregister:
			print("% -> Register component #{:d} - {:s}".format(msg.Id, msg.Type))
			components.add(msg)
		else:
			print("% -> Deregister component #{:d} - {:s}".format(msg.Id, msg.Type))
			component = components.get(msg.Id)
			component.dead = True
			problems.release(component.id)
	elif type(msg) == messages.SolveRequest:
		print("% -> SolveRequest")
		problems.add(msg)
	elif type(msg) == messages.SolvePartialProblems:
		print("% -> SolvePartialProblems")
		problem = problems.list[msg.Id]
		problem.updateWithDivide(msg)
	elif type(msg) == messages.Solutions:
		print("% -> Solutions")
		problem = problems.list[msg.Id]
		problem.updateWithSolutions(msg)
	elif type(msg) == messages.NoOperation:
		print("% -> NoOperation")
		# update backup server list
	else:
		print("% ? {:s}".format(str(msg)))

def keepAlive():
	while True:
		try:
			# Wait keepAlive period
			time.sleep(config.timeout / 2)
		except:
			break

		# Connect to master and ask for status
		print("{time:s} Send KeepAlive".format(time=Utilities.current_time_formatted()))
		try:
			conn = messages.Connection(socket.create_connection((config.parent_address, config.parent_port)))
			connections_manager.add(conn)
			msg = messages.Status(config.id, [])
			conn.send(msg)
			# Inform parent about lower backup registrations and deregistrations
			for msg in backup_servers.getParentMessages():
				conn.send(msg)
			conn.socket.shutdown(socket.SHUT_WR)

			# Read all messages from client separated by 0x17 until EOC (write stream closed)
			for msg in conn:
				parseMessageBCS(msg)

			conn.socket.close()
			connections_manager.remove(conn)
		except OSError as msg:
			print("KeepAlive connection error: {:s}".format(str(msg)))
			print("Assuming main communication server role")
			# Refresh components timeout, else when assume main cs role all would be thought dead
			for component in components.active():
				component.touch()
			config.is_backup = False
			break

def registerBackup(address, port, assumeId=None):
	print("{time:s} Connecting to {address:s}:{port:d}...".format(time=Utilities.current_time_formatted(), address=address, port=port))
	while True:
		try:
			conn = messages.Connection(connect((address, port), ('::', args.port)))
			connections_manager.add(conn)
			break
		except Exception as msg:
			print("Trying to bind...")
			time.sleep(1)

	print("Send Register message")
	request = messages.Register(Type="CommunicationServer", SolvableProblems=[], ParallelThreads=0, Id=assumeId)
	conn.send(request)
	conn.socket.shutdown(socket.SHUT_WR)

	for msg in conn:
		if type(msg) == messages.RegisterResponse:
			# Has BackupCommunicationServers field -> connect to next backup in list
			if msg.BackupCommunicationServers:
				backup = msg.BackupCommunicationServers[0]
				print("Sent to next BCS at {address:s}:{port:d}".format(address=backup['address'], port=backup['port']))
				conn.socket.close()
				connections_manager.remove(conn)
				registerBackup(backup['address'], backup['port'], msg.Id)
				return
			# Registered at last communication server in list
			else:
				print("Registered successfully")
				config.id = msg.Id
				config.timeout = msg.Timeout
				config.parent_address = address
				config.parent_port = port
		# Messages with state, sent from higher communication server
		else:
			parseMessageBCS(msg)

	conn.socket.close()
	connections_manager.remove(conn)

# Main

if not args.backup:
	runServer()
else:
	print("Starting backup server on port {port:d}".format(port=args.port))
	# try:
	registerBackup(args.primary_address, args.primary_port)
	threading.Thread(target=keepAlive).start()
	runServer()
	# except OSError as msg:
	# 	print("Connection exception: ", msg)
