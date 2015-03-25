from argparse import ArgumentParser, Namespace
import sys
import socket
import time
import threading
import signal as os_signal
from time import strftime
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
config.master = (args.address, args.port)
config.backup_masters = []

def keepAlive():
	while True:
		# Wait keepAlive period
		time.sleep(config.timeout/2)

		# Connect to master and ask for status
		print("{time:s} Send KeepAlive".format(time=strftime("%H:%M:%S")))
		conn = messages.Connection(socket.create_connection(config.master))
		connections.append(conn)
		conn.send(messages.Status(config.id, [])) # TODO threads
		conn.socket.shutdown(socket.SHUT_WR)

		# Read response
		for msg in conn:
			if type(msg) == messages.NoOperation:
				print("Response: NoOperation")
				config.backup_masters = msg.BackupCommunicationServers

			elif type(msg) == messages.DivideProblem:
				print("Response: DivideProblem")
				# TODO DivideProblem!
				pass

def register():
	print("Try to connect...")
	conn = messages.Connection(socket.create_connection(config.master))
	connections.append(conn)
	print("Send Register message")
	conn.send(messages.Register("TaskManager" if args.type == "TM" else "ComputationalNode", ["TSP"], 8))
	conn.socket.shutdown(socket.SHUT_WR)
	for msg in conn:
		if type(msg) == messages.RegisterResponse:
			print("Registered successfully")
			config.id = msg.Id
			config.timeout = msg.Timeout
			config.backup_masters = msg.BackupCommunicationServers

connections = []

# Close connection on ctrl+c
def signal_handler(signal, frame):
    print('Closing connections and exiting...')
    for conn in connections:
    	conn.socket.close()
    sys.exit(0)

os_signal.signal(os_signal.SIGINT, signal_handler)

# Run
register()
keepAlive()
