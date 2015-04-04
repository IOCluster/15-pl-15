from argparse import Namespace
import Register as reg

#SEPARATOR = b"\x17"	# == ctrl+w
SEPARATOR = b"\n"

class Connection:
	def __init__(self, socket, timeout=None):
		self.socket = socket
		if timeout:
			self.socket.settimeout(timeout)

	def send(self, message):
		self.socket.send(message + SEPARATOR)

	# Iterate over messages separated by SEPARATOR, break after recv 0 bytes
	def __iter__(self):
		buf = b""
		while True:
			data = self.socket.recv(8192)
			if not data: break
			if SEPARATOR in data:
				yield parse(buf + data[:data.find(SEPARATOR)])
				buf = data[data.find(SEPARATOR) + 1:]
			else:
				buf += data


class NamespaceEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Namespace):
			return o.__dict__

class Message(Namespace):
	Types = dict()

	def __str__(self)
		return self.toxml()
	def __bytes__(self):
		return str(self).encode("utf-8")

	def __add__(self, other):
		if type(other) == bytes:
			return bytes(self) + other
		return Namespace.__add__(self, other)

	def __radd__(self, other):
		if type(other) == bytes:
			return other + bytes(self)
		return Namespace.__radd__(self, other)


class Register(Message):
class Register(Message):
	def __init__(self, Type, SolvableProblems, ParallelThreads, Deregister=None, Id=None):
            mes = reg.CreateFromDocument("\
                    <?xml version=\"1.0\" encoding=\"utf-8\" ?>\
                    <Register  xmlns=\"http://www.mini.pw.edu.pl/ucc/\"\
                    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\
                    xsi:noNamespaceSchemaLocation=\"Register.xsd\">\
                    <Type>TaskManager</Type>\
                    <SolvableProblems>\
                        <ProblemName>DVRP</ProblemName>\
                    </SolvableProblems>\
                    <ParallelThreads>8</ParallelThreads>\
                    <Deregister>false</Deregister>\
                    <Id>12</Id>\
                    </Register>")
            mes.Type = Type
            mes.ParallelThreads = ParallelThreads
            mes.Deregister = Deregister
            mes.Id = Id



