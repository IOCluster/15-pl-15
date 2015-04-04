from argparse import ArgumentParser
import random
import sys
import threading
import socket
import signal
from time import strftime
from iocluster import messages
from iocluster.master.component import components
from iocluster.master.task import tasks
from iocluster.util import connections_manager

argfix = {
	"-port": "--port",
	"-backup": "--backup",
}

args = [(x if not x in argfix else argfix[x]) for x in sys.argv[1:]]
parser = ArgumentParser(prog=sys.argv[0], description="Master server")
parser.add_argument('--port', '-p', type=int, default=2121, help="port to listen on")
parser.add_argument('--backup', '-b', action="store_true", help="are we a backup server?")
parser.add_argument('--timeout', '-t', type=int, default=5, help="component timeout (s)")
args = parser.parse_args(args)

# The important
# information that are synchronized are the existing CN and TM and their current activities and the data of
# tasks, partial problems, partial solutions and final solutions. Each backup server connects first with the
# main CS but if it is not the first backup server it registers with the current last backup server. In that way,
# each backup server needs to store only one set of data to be synchronized. The current information is
# sent to the backup CS when it registers with the CS of a higher level and is updated after each

# [Register or data message
# message
# Received || Inactive component removed
# => Add information to
# synchronization
# queue and update
# internal information

# Synchronize state with first backup server
def asyncSynchronize():
	pass

def messageRegister(conn, msg):
	id = components.add(conn, msg)
	print("Register: {type:s} (Id: {id:d})".format(type=msg.Type, id=id))
	response = messages.RegisterResponse(id, args.timeout, [])
	conn.send(response)

def messageStatus(conn, msg):
	assert msg.Id < len(components.list), "component id not registered"
	assert not components.list[msg.Id].dead, "component already dead"
	component = components.list[msg.Id]
	component.touch()
	component.parseStatus(msg)
	component.sendMessages(conn)

def messageSolveRequest(conn, msg):
	id = tasks.add(msg)
	print("-> AddTask :: #{id:d} Type: {type:s} Timeout: {timeout:d}".format(type=msg.ProblemType, timeout=msg.SolvingTimeout, id=id))
	response = messages.SolveRequestResponse(id)
	conn.send(response)

def messageSolutionRequest(conn, msg):
	assert msg.Id < len(tasks.list), "task id not registered"
	task = tasks.list[msg.Id]
	response = task.getSolutionRequestMessage()
	conn.send(response)

def handleConnection(conn):
	print("{time:s} Connection from {server:s}:{port:d}".format(time=strftime("%H:%M:%S"), server=conn.socket.getpeername()[0], port=conn.socket.getpeername()[1]))
	try:
		# Read all messages from client separated by 0x17 until EOC (write stream closed)
		for msg in conn:
			print("+ {:s}".format(str(msg)))
			if type(msg) == messages.Register:
				messageRegister(conn, msg)
			elif type(msg) == messages.Status:
				messageStatus(conn, msg)
			elif type(msg) == messages.SolveRequest:
				messageSolveRequest(conn, msg)
			elif type(msg) == messages.SolutionRequest:
				messageSolutionRequest(conn, msg)
	except AssertionError as e:
		print("Assertion error: {0}".format(e))
	except Exception as e:
		print('Exception occurred:', e)
	# Close connection
	conn.socket.close()
	connections_manager.remove(conn)

def removeInactiveComponents():
	for index, component in enumerate(components.list):
		# Wait twice the timeout, as nodes are sending state each timeout seconds
		if not component.dead and not component.isAlive(2 * args.timeout * 1000):
			print("Removing inactive component: #{:d} ({:s})".format(component.id, type(component).__name__))
			# asyncSynchronize()

signal.signal(signal.SIGINT, lambda: connections_manager.closeAndExit())

# Open server socket
print("Starting server on port {port:d} with timeout {timeout:d}".format(port=args.port, timeout=args.timeout))
server = socket.socket(socket.AF_INET6)
server.bind(("::", args.port))
server.listen(50)

# Main Loop: Listen for incoming connections
while True:
	try:
		s, addr = server.accept()
	except:
		break
	removeInactiveComponents()
	conn = messages.Connection(s, timeout=args.timeout)
	connections_manager.add(conn)
	threading.Thread(target=handleConnection, args=(conn,)).start()
