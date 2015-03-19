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
args = parser.parse_args(args)

master = messages.Connection(socket.create_connection((args.address, args.port)))
master.send(messages.SolveRequest("TSP", "SWRlYWx5IHNhIGphayBnd2lhemR5IC0gbmllIG1vem5hIGljaCBvc2lhZ25hYywgYWxlIG1vem5hIHNpZSBuaW1pIGtpZXJvd2FjLg0K"))
print("Problem ID: " + str(next(iter(master)).Id))
