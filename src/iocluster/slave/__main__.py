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
parser.add_argument('--type', '-t', type=str, default="CN", help="TM/CN")
parser.add_argument('--address', '-a', type=str, help="IPv4/6 address or host name to connect to")
parser.add_argument('--port', '-p', type=int, default=2121, help="port to connect to")
args = parser.parse_args(args)

config = Namespace()
config.id = None
config.timeout = None
config.master = None
config.backup_masters = []

def handleMessages(config):
	for msg in config.master:
		print(str(msg))
		if type(msg) == messages.NoOperation:
			config.backup_masters = msg.BackupCommunicationServers
		elif type(msg) == messages.RegisterResponse:
			config.id = msg.Id
			config.timeout = msg.Timeout
			config.backup_masters = msg.BackupCommunicationServers
			threading.Thread(target=lambda: sendStatuses(config)).start()

def sendStatuses(config):
	while True:
		time.sleep(config.timeout/2)
		config.master.send(messages.Status(config.id, [])) # TODO threads

config.master = messages.Connection(socket.create_connection((args.address, args.port)))
config.master.send(messages.Register("TaskManager" if args.type == "TM" else "ComputationalNode", ["TSP"], 8))
handleMessages(config)
