from argparse import ArgumentParser, Namespace
import signal
import socket
import sys
import time
import threading
from iocluster import messages
from iocluster.util import ConnectionsManager
import iocluster.util as Utilities

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

config = Namespace()
config.id = None
config.sleep = 2

connections_manager = ConnectionsManager()
signal.signal(signal.SIGINT, lambda: connections_manager.closeAndExit())

def checkForSolutions():
	while True:
		# Connect to master and ask for solution
		print("{time:s} Send SolutionRequest for problem #{id:d}".format(time=Utilities.current_time_formatted(), id=args.problem_id))
		conn = messages.Connection(socket.create_connection((args.address, args.port)))
		connections_manager.add(conn)
		conn.send(messages.SolutionRequest(args.problem_id))
		conn.socket.shutdown(socket.SHUT_WR)

		# Read response
		for msg in conn:
			if type(msg) == messages.Solutions:
				assert hasattr(msg, 'Solutions') and len(msg.Solutions) > 0, "solutions message invalid"
				if msg.Solutions[0].Type == "Ongoing":
					print("Computing...")

				# Timeout occured
				elif msg.Solutions[0].Type == "Partial":
					print("Partial received")
					return True

				elif msg.Solutions[0].Type == "Final":
					print("Solution received")
					return True

		connections_manager.remove(conn)

		try:
			# Sleep for some amount of time
			time.sleep(config.sleep)
		except:
			break

if checkForSolutions():
	# Save soluition to disk
	pass
