from argparse import ArgumentParser
import sys
import socket
import threading
from iocluster import messages
from iocluster.master.slave import Slave

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

server = socket.socket(socket.AF_INET6)
server.bind(("::", args.port))
server.listen(50)

components = []
problems = []

def handleConnection(c):
	id = len(components)
	components.append(None)
	try:
		for msg in c:
			print(str(msg))

			if type(msg) == messages.Register:
				if msg.Type in Slave.Types:
					components[id] = Slave.Types[msg.Type](c, msg.SolvableProblems, msg.ParallelThreads)
					c.send(messages.RegisterResponse(id, args.timeout, [])) # TODO backup
				elif msg.Type == "CommunicationServer":
					return # TODO

			elif type(msg) == messages.Status:
				assert(msg.Id == id)
				# TODO msg.Threads?
				c.send(messages.NoOperation([])) # TODO backup

			elif type(msg) == messages.SolveRequest:
				problem_id = len(problems)
				problems.append(msg) # TODO do something useful
				c.send(messages.SolveRequestResponse(problem_id))

	except OSError: # eg. timeout or socket closure
		# This one is dead.
		components[id] = None

while True:
	s, addr = server.accept()
	threading.Thread(target=handleConnection, args=(messages.Connection(s, timeout=args.timeout),)).start()
