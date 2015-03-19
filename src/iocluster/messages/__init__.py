from argparse import Namespace
import json

#SEPARATOR = b"\x17"
SEPARATOR = b"\n"

class Connection:
	def __init__(self, socket, timeout=None):
		self.socket = socket
		self.buffer = b""
		if timeout:
			self.socket.settimeout(timeout)

	def send(self, message):
		self.socket.send(message + SEPARATOR)

	def __iter__(self):
		while True:
			while SEPARATOR in self.buffer:
				msg, self.buffer = self.buffer.split(SEPARATOR, 1)

				yield(parse(msg))
			self.buffer += self.socket.recv(4096)

# TODO Support that XML shit.

class Message(Namespace):
	Types = dict()

	def __str__(self):
		return type(self).__name__ + " " + json.dumps(self.__dict__)

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
	def __init__(self, Type, SolvableProblems, ParallelThreads, Deregister=None, Id=None):
		Namespace.__init__(self, Type=Type, SolvableProblems=SolvableProblems, ParallelThreads=ParallelThreads, Deregister=Deregister, Id=Id)
Message.Types["Register"] = Register

class RegisterResponse(Message):
	def __init__(self, Id, Timeout, BackupCommunicationServers):
		Namespace.__init__(self, Id=Id, Timeout=Timeout, BackupCommunicationServers=BackupCommunicationServers)
Message.Types["RegisterResponse"] = RegisterResponse

class Status(Message):
	def __init__(self, Id, Threads):
		Namespace.__init__(self, Id=Id, Threads=Threads)
Message.Types["Status"] = Status

class NoOperation(Message):
	def __init__(self, BackupCommunicationServers):
		Namespace.__init__(self, BackupCommunicationServers=BackupCommunicationServers)
Message.Types["NoOperation"] = NoOperation

class SolveRequest(Message):
	def __init__(self, ProblemType, Data, SolvingTimeout=None, Id=None):
		Namespace.__init__(self, ProblemType=ProblemType, Data=Data, SolvingTimeout=SolvingTimeout, Id=Id)
Message.Types["SolveRequest"] = SolveRequest

class SolveRequestResponse(Message):
	def __init__(self, Id):
		Namespace.__init__(self, Id=Id)
Message.Types["SolveRequestResponse"] = SolveRequestResponse

def parse(message):
	message = message.decode("utf-8")
	t, data = message.split(" ", 1)
	data = json.loads(data)
	if type(data) == dict:
		return Message.Types[t](**data)
	else:
		return Message.Types[t](*data)