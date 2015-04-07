import time
import socket
from time import strftime

current_time_ms = lambda: int(round(time.time() * 1000))
current_time_formatted = lambda: strftime("%H:%M:%S")

class ConnectionsManager:
	def __init__(self):
		self.connections = []

	def add(self, conn):
		self.connections.append(conn)

	def remove(self, conn):
		if conn in self.connections:
			self.connections.remove(conn)

	def closeAndExit(self, f):
	    print('Closing connections and exiting...')
	    for conn in self.connections:
	    	conn.socket.close()
	    sys.exit(0)

connections_manager = ConnectionsManager()

# Same as socket.create_connection, but with default timeout and SO_REUSEADDR
def connect(dest, source=None):
    host, port = dest
    err = None
    for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket.socket(af, socktype, proto)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(socket.getdefaulttimeout())
            if source:
                sock.bind(source)
            sock.connect(sa)
            return sock

        except Exception as _:
            err = _
            if sock is not None:
                sock.close()
    if err is not None:
        raise err
    else:
        raise Exception("getaddrinfo returns an empty list")
