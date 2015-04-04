from argparse import ArgumentParser, Namespace
import sys
import socket
import time
import threading
from random import randint
import signal as signal
from time import strftime
from iocluster import messages
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
config.master = (args.address, args.port)
config.backup_masters = []

connections_manager = Utilities.ConnectionsManager()

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

		connections_manager.remove(conn)

def register():
	print("{time:s} Connecting to ...".format(time=Utilities.current_time_formatted()))
	conn = messages.Connection(socket.create_connection(config.master))
	connections_manager.add(conn)
	print("Send Register message")
	conn.send(messages.Register("TaskManager" if args.type == "TM" else "ComputationalNode", ["TSP"], 8))
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
