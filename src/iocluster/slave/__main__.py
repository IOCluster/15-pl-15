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
config.threads = 8
config.problems = ["TSP"]
config.master = (args.address, args.port)
config.backup_masters = []

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

current_task = None
current_task_started = 0

def messageNoOperation(msg):
	print("Response: NoOperation")
	# config.backup_masters = msg.BackupCommunicationServers

# TODO MergeSolutions
def mergeSolutions(msg):
	global current_task
	problemType = msg.ProblemType
	problemId = msg.Id
	commonData = msg.CommonData
	for solution in msg.Solutions:
		taskId = solution.TaskId
		timeoutOccured = solution.TimeoutOccured
		solutionType = solution.Type
		computationsTime = solution.ComputationsTime
		solutionData = solution.Data
	try:
		time.sleep(3)
	except:
		pass
	solutions = [{
		"TimeoutOccured": False,
		"Type": "Final", # Partial
		"ComputationsTime": 0,
		"Data": "mergedData"
	}]
	message = messages.Solutions(msg.Id, msg.ProblemType, solutions)
	pending_messages.add(message)
	current_task = None

def messageSolutions(msg):
	print("Response: MergeSolution")
	global current_task, current_task_started
	current_task = msg
	current_task_started = current_time_ms()
	threading.Thread(target=mergeSolutions, args=(msg,)).start()

# TODO DivideProblem!
def divideProblem(msg):
	global current_task
	problemType = msg.ProblemType
	problemId = msg.Id
	problemData = msg.Data
	threadCount = msg.ComputationalNodes
	thisId = msg.NodeID
	try:
		time.sleep(3)
	except:
		pass
	commonData = "data"
	partialProblems = []
	partialProblems.append({
		"TaskId": 0,
		"Data": "data_sub",
		"NodeID": config.id
	})
	message = messages.SolvePartialProblems(msg.Id, msg.ProblemType, commonData, partialProblems)
	pending_messages.add(message)
	current_task = None

def messageDivideProblem(msg):
	print("Response: DivideProblem")
	global current_task, current_task_started
	current_task = msg
	current_task_started = current_time_ms()
	threading.Thread(target=divideProblem, args=(msg,)).start()

def solvePartialProblem(msg):
	global current_task
	problemType = msg.ProblemType
	problemId = msg.Id
	commonData = msg.CommonData
	solvingTimeout = msg.SolvingTimeout
	# for partialProblem in msg.PartialProblems:
	partialProblem = msg.PartialProblems[0]
	taskId = partialProblem.TaskId
	data = partialProblem.Data
	tmNodeId = partialProblem.NodeID
	try:
		time.sleep(3)
	except:
		pass
	solutions = [] # Type=Partial
	solution = messages.Solution(Type="Final", ComputationsTime=(current_time_ms() - current_task_started), TimeoutOccured=False, TaskId=taskId, Data="solution")
	solutions.append(solution)
	message = messages.Solutions(problemId, msg.ProblemType, solutions, msg.CommonData)
	pending_messages.add(message)
	current_task = None

def messageSolvePartialProblems(msg):
	print("Response: SolvePartialProblems")
	global current_task, current_task_started
	current_task = msg
	current_task_started = current_time_ms()
	threading.Thread(target=solvePartialProblem, args=(msg,)).start()

def getStatusMessage():
	threads = []
	# for i in range(config.threads):
	thread = {}
	if current_task == None:
		thread["State"] = "Idle"
	else:
		thread["State"] = "Busy"
		thread["ProblemType"] = current_task.ProblemType
		thread["HowLong"] = current_time_ms() - current_task_started
		thread["ProblemInstanceId"] = current_task.Id
		if not args.type == "TM":
			thread["TaskId"] = 0 # TODO
	threads.append(thread)
	msg = messages.Status(config.id, threads) # TODO threads
	return msg

def keepAlive():
	while True:
		try:
			# Wait keepAlive period
			time.sleep(config.timeout/2)
		except:
			break

		# Simulate dying
		#if (randint(0, 10) == 0):
		#	return

		# Connect to master and ask for status
		print("{time:s} Send KeepAlive".format(time=Utilities.current_time_formatted()))
		conn = messages.Connection(socket.create_connection(config.master))
		connections_manager.add(conn)
		request = getStatusMessage()
		conn.send(request)
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

		connections_manager.remove(conn)

def register():
	print("{time:s} Connecting to ...".format(time=Utilities.current_time_formatted()))
	conn = messages.Connection(socket.create_connection(config.master))
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
			config.backup_masters = msg.BackupCommunicationServers

	connections_manager.remove(conn)

# Close connection on ctrl+c
signal.signal(signal.SIGINT, lambda: connections_manager.closeAndExit())

# Run
register()
keepAlive()
