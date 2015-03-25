from argparse import ArgumentParser
import random
import sys
import threading
import socket
import signal as os_signal
from time import strftime
from iocluster import messages
from iocluster.master.slave import Slave
from iocluster.master.sig import Signal

argfix = {
	"-port": "--port",
	"-backup": "--backup",
}

args = [(x if not x in argfix else argfix[x]) for x in sys.argv[1:]]
parser = ArgumentParser(prog=sys.argv[0], description="Master server")
parser.add_argument('--port', '-p', type=int, default=2121, help="port to listen on")
parser.add_argument('--backup', '-b', action="store_true", help="are we a backup server?")
parser.add_argument('--timeout', '-t', type=int, default=5, help="component timeout")
args = parser.parse_args(args)

TMs = []
CNs = []
BCSs = []
component_added = Signal()
tasks = []

class Task:
	New = 0
	Divided = 1
	Merging = 2
	Done = 3

def advanceTask(task):
	try:
		task.state
	except:
		task.state = Task.New
		task.divider = None

	if task.state == Task.New and not task.divider:
		usable_slaves = [x for x in components if x and x.DivideProblem and task.ProblemType in x.problems]
		if not usable_slaves:
			print("No usable slave, queueing.")
			component_added.queue(lambda: advanceTask(task))
			return

		task.divider = random.choice(usable_slaves)
		task.divider.DivideProblem(task, 10) # TODO Number of threads in the whole cluster
		def redivide(task):
			 task.divider = None
			 advanceTask(task)
		task.divider.died.queue(lambda: redivide(task))

def handleConnection(c):
	print("{time:s} Connection from {server:s}:{port:d}".format(time=strftime("%H:%M:%S"), server=c.socket.getpeername()[0], port=c.socket.getpeername()[1]))
	try:
		# Read all messages from client separated by 0x17 until EOC (write stream closed)
		for msg in c:
			print("Received: {:s}".format(str(msg)))

			if type(msg) == messages.Register:
				print("Register: {type:s}".format(type=msg.Type))
				if msg.Type == "TaskManager":
					id = len(TMs)
					TMs.append(Slave.Types[msg.Type](id, c, msg.SolvableProblems, msg.ParallelThreads))
					c.send(messages.RegisterResponse(id, args.timeout, [])) # TODO backup
				# if msg.Type in Slave.Types:
				# 	components[id] = Slave.Types[msg.Type](id, c, msg.SolvableProblems, msg.ParallelThreads)
				# 	c.send(messages.RegisterResponse(id, args.timeout, [])) # TODO backup
				# 	component_added.notify_all()
				elif msg.Type == "CommunicationServer":
					return # TODO

			elif type(msg) == messages.Status:
				# assert(msg.Id == id)
				# TODO msg.Threads?
				c.send(messages.NoOperation([])) # TODO backup

			elif type(msg) == messages.SolveRequest:
				# TODO think about copying data from SolveRequest to a new Task class.
				msg.Id = len(tasks)
				tasks.append(msg)
				advanceTask(msg)
				c.send(messages.SolveRequestResponse(msg.Id))

			elif type(msg) == messages.SolutionRequest:
				try:
					task = tasks[msg.Id]
				except KeyError:
					# Unknown task.
					# Documentation didn't say what to do now.
					# So close connection.
					return
				c.send(messages.Solutions(task.Id, task.ProblemType, task.Data, [dict(Type="Ongoing", ComputationsTime=0)])) # TODO SolveRequest.Data == CommonData?

	except Exception as e:
		print 'Exception occurred:', e
	# except: # eg. timeout or socket closure
		# This one is dead.
		# pass

	# Close connection
	c.socket.close()
	connections.remove(c)

	# if components[id]:
	# 	c = components[id]
	# 	components[id] = None
	# 	c.died.notify_all()

connections = []

# Close connection on ctrl+c
def signal_handler(signal, frame):
    print('Closing connections and exiting...')
    for conn in connections:
    	conn.socket.close()
    sys.exit(0)

os_signal.signal(os_signal.SIGINT, signal_handler)

# Open server socket
server = socket.socket(socket.AF_INET6)
server.bind(("::", args.port))
server.listen(50)

# Main Loop: Listen for incoming connections
while True:
	s, addr = server.accept()
	conn = messages.Connection(s, timeout=args.timeout)
	connections.append(conn)
	threading.Thread(target=handleConnection, args=(conn,)).start()
