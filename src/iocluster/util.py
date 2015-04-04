import time
from time import strftime

current_time_ms = lambda: int(round(time.time() * 1000))
current_time_formatted = lambda: strftime("%H:%M:%S")

class ConnectionsManager:
	def __init__(self):
		self.connections = []

	def add(self, conn):
		self.connections.append(conn)

	def remove(self, conn):
		self.connections.remove(conn)

	def closeAndExit(self, f):
	    print('Closing connections and exiting...')
	    for conn in self.connections:
	    	conn.socket.close()
	    sys.exit(0)

connections_manager = ConnectionsManager()
