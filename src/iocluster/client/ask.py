from argparse import ArgumentParser, Namespace
import sys
import socket
import time
import threading
from iocluster import messages

argfix = {
	"-address": "--address",
	"-port": "--port",
}

args = [(x if not x in argfix else argfix[x]) for x in sys.argv[1:]]
parser = ArgumentParser(prog=sys.argv[0], description="Slave server")
parser.add_argument('--address', '-a', type=str, help="IPv4/6 address or host name to connect to")
parser.add_argument('--port', '-p', type=int, default=2121, help="port to connect to")
parser.add_argument('problem_id', type=int, help="problem ID to ask about")
args = parser.parse_args(args)

master = messages.Connection(socket.create_connection((args.address, args.port)))
master.send(messages.SolutionRequest(args.problem_id))
print("Answer: " + str(next(iter(master))))
