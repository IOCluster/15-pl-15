from argparse import ArgumentParser, Namespace
import sys
import socket
import time
import threading
from iocluster import messages
import base64

argfix = {
	"-address": "--address",
	"-port": "--port",
}

args = [(x if not x in argfix else argfix[x]) for x in sys.argv[1:]]
parser = ArgumentParser(prog=sys.argv[0], description="Slave server")
parser.add_argument('--address', '-a', type=str, help="IPv4/6 address or host name to connect to")
parser.add_argument('--port', '-p', type=int, default=2121, help="port to connect to")
parser.add_argument('--type', '-t', type=str, default="Dummy", help="problem type")
parser.add_argument('--file', '-f', type=str, help="data file name")
parser.add_argument('--data', '-d', type=str, default="3", help="data string")

args = parser.parse_args(args)

if args.file:
	args.data = open(args.file).read()

master = messages.Connection(socket.create_connection((args.address, args.port)))
request = messages.SolveRequest(args.type, args.data, SolvingTimeout=10)
master.send(request)
print("Problem ID: " + str(next(iter(master)).Id))
