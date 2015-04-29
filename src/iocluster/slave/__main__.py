from argparse import ArgumentParser, Namespace
import sys
import socket
import time
import threading
from random import randint
import signal as signal
from time import strftime
from iocluster import messages
from iocluster.util import current_time_ms
import iocluster.util as Utilities

from dummysolver import TaskSolver

argfix = {
	"-address": "--address",
	"-port": "--port",
}

args = [(x if not x in argfix else argfix[x]) for x in sys.argv[1:]]
parser = ArgumentParser(prog=sys.argv[0], description="Slave server")
parser.add_argument('--type', '-t', type=str, default="CN", help="TM/CN")
parser.add_argument('--address', '-a', type=str, help="IPv4/6 address or host name to connect to")
parser.add_argument('--port', '-p', type=int, default=2121, help="port to connect to")
args = parser.parse_args(args)

config = Namespace()
config.id = None
config.timeout = None
config.threads = 2
config.problems = ["TSP"]
config.master = { "address": args.address, "port": args.port }
config.backups = []

connections_manager = Utilities.ConnectionsManager()

class PendingMessages:
	list = []
	lock = threading.Lock()

	def add(self, msg):
		self.lock.acquire()
		try:
			self.list.append(msg)
		finally:
			self.lock.release()

	def getAll(self):
		self.lock.acquire()
		try:
			messages = list(self.list)
			self.list = []
			return messages
		finally:
			self.lock.release()

pending_messages = PendingMessages()

class OpThread:
	def __init__(self, msg, assignedId):
		self.started = current_time_ms()
		self.message = msg
		self.assignedId = assignedId

threads = []

def messageNoOperation(msg):
	print("Response: NoOperation")
	config.backups = msg.BackupCommunicationServers

def mergeSolutions(thread):
	msg = thread.message
	problemType = msg.ProblemType

	solver = TaskSolver(msg.CommonData)
	value = solver.merge(list(solution.Data for solution in msg.Solutions))
	sumTime = sum(int(solution.ComputationsTime) for solution in msg.Solutions)

	solutions = [{
		"TimeoutOccured": False,
		"Type": "Final", # Partial
		"ComputationsTime": current_time_ms() - thread.started + sumTime,
		"Data": str(value)
	}]
	message = messages.Solutions(msg.Id, msg.ProblemType, solutions, msg.CommonData)
	pending_messages.add(message)
	threads.remove(thread)

def messageSolutions(msg):
	print("Response: MergeSolution")
	thread = OpThread(msg, msg.Id)
	threads.append(thread)
	threading.Thread(target=mergeSolutions, args=(thread,)).start()

def divideProblem(thread):
	msg = thread.message
	problemType = msg.ProblemType

	solver = TaskSolver(msg.Data)
	partialProblems = [{
		"TaskId": i,
		"Data": str(problem),
		"NodeID": config.id
	} for i, problem in enumerate(solver.divide(msg.ComputationalNodes))]

	message = messages.SolvePartialProblems(msg.Id, msg.ProblemType, msg.Data, partialProblems)
	pending_messages.add(message)
	threads.remove(thread)

def messageDivideProblem(msg):
	print("Response: DivideProblem")
	thread = OpThread(msg, msg.Id)
	threads.append(thread)
	threading.Thread(target=divideProblem, args=(thread,)).start()

def solvePartialProblem(thread):
	msg = thread.message
	problemType = msg.ProblemType
	partialProblem = [item for item in msg.PartialProblems if item.TaskId == thread.assignedId][0]

	solver = TaskSolver(msg.CommonData)
	data = solver.solve(partialProblem.Data, msg.SolvingTimeout)

	solutions = [] # Type=Partial
	solution = messages.Solution(Type="Final", ComputationsTime=(current_time_ms() - thread.started), TimeoutOccured=False, TaskId=partialProblem.TaskId, Data=data)
	solutions.append(solution)
	message = messages.Solutions(msg.Id, msg.ProblemType, solutions, msg.CommonData)
	pending_messages.add(message)
	threads.remove(thread)

def messageSolvePartialProblems(msg):
	print("Response: SolvePartialProblems")
	for task in msg.PartialProblems:
		thread = OpThread(msg, task.TaskId)
		threads.append(thread)
		threading.Thread(target=solvePartialProblem, args=(thread,)).start()

def sendStatusMessage(conn):
	msgThreads = []
	for thread in threads:
		msgThread = {
			"State": "Busy",
			"ProblemType": thread.message.ProblemType,
			"HowLong": current_time_ms() - thread.started,
			"ProblemInstanceId": thread.message.Id
		}
		if not args.type == "TM":
			msgThread["TaskId"] = thread.assignedId
		msgThreads.append(msgThread)
	for i in range(config.threads - len(threads)):
		msgThreads.append({
			"State": "Idle"
		})	
	msg = messages.Status(config.id, msgThreads)
	conn.send(msg)

def keepAlive():
	server = config.master
	while True:
		try:
			# Wait keepAlive period
			time.sleep(config.timeout/2)
		except:
			break

		# Simulate dying
		#if (randint(0, 10) == 0):
		#	return

		try:
			# Connect to master and ask for status
			print("{time:s} Send KeepAlive".format(time=Utilities.current_time_formatted()))
			conn = messages.Connection(Utilities.connect((server["address"], server["port"])))
			connections_manager.add(conn)
			sendStatusMessage(conn)
			for msg in pending_messages.getAll():
				print("Sending result: {:s}".format(str(msg)))
				conn.send(msg)
			conn.socket.shutdown(socket.SHUT_WR)

			# Read response
			for msg in conn:
				# TM, CN: Backup servers info
				if type(msg) == messages.NoOperation:
					messageNoOperation(msg)
				# TM: Divide problem
				elif type(msg) == messages.DivideProblem:
					messageDivideProblem(msg)
				# CN: Compute partial problems solutions
				elif type(msg) == messages.SolvePartialProblems:
					messageSolvePartialProblems(msg)
				# TM: Merge partial solutions
				elif type(msg) == messages.Solutions:
					messageSolutions(msg)
				else:
					print("? {:s}".format(str(msg)))

			conn.socket.close()
			connections_manager.remove(conn)

		except OSError as msg:
			print("KeepAlive connection error: {:s}".format(str(msg)))
			if config.backups:
				index = config.backups.index(server) if server in config.backups else -1
				server = config.backups[index + 1] if len(config.backups) > index + 1 else None
				if server == None:
					print("No further backup servers available, exiting...")
					break
				print("Backup list: ", config.backups)
				print("Connecting to next backup: {:s}:{:d}".format(server["address"], server["port"]))
			else:
				break

def register():
	print("{time:s} Connecting to ...".format(time=Utilities.current_time_formatted()))
	conn = messages.Connection(socket.create_connection((config.master["address"], config.master["port"])))
	connections_manager.add(conn)
	print("Send Register message")
	request = messages.Register("TaskManager" if args.type == "TM" else "ComputationalNode", config.problems, config.threads)
	conn.send(request)
	conn.socket.shutdown(socket.SHUT_WR)
	
	for msg in conn:
		if type(msg) == messages.RegisterResponse:
			print("Registered successfully")
			config.id = msg.Id
			config.timeout = msg.Timeout
			config.backups = msg.BackupCommunicationServers

	connections_manager.remove(conn)

# Close connection on ctrl+c
signal.signal(signal.SIGINT, lambda: connections_manager.closeAndExit())

# Run
register()
keepAlive()
