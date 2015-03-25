from argparse import Namespace
import json

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

# TODO Support that XML shit.

class NamespaceEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Namespace):
			return o.__dict__

class Message(Namespace):
	Types = dict()

	def __str__(self):
		return type(self).__name__ + " " + json.dumps(self.__dict__, cls=NamespaceEncoder)

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

class SolutionRequest(Message):
	def __init__(self, Id):
		Namespace.__init__(self, Id=Id)
Message.Types["SolutionRequest"] = SolutionRequest

class Solution(Namespace):
	def __init__(self, Type, ComputationsTime, TimeoutOccured=False, TaskId=None, Data=None):
		Namespace.__init__(self, TaskId=TaskId, TimeoutOccured=TimeoutOccured, Type=Type, ComputationsTime=ComputationsTime, Data=Data)

class Solutions(Message):
	def __init__(self, Id, ProblemType, CommonData, Solutions):
		Solutions = [x if isinstance(x, Solution) else Solution(**x) for x in Solutions]
		Namespace.__init__(self, ProblemType=ProblemType, Id=Id, CommonData=CommonData, Solutions=Solutions)
Message.Types["Solutions"] = Solutions

class DivideProblem(Message):
	def __init__(self, Id, ProblemType, Data, ComputationalNodes, NodeID):
		Namespace.__init__(self, ProblemType=ProblemType, Id=Id, Data=Data, ComputationalNodes=ComputationalNodes, NodeID=NodeID)
Message.Types["DivideProblem"] = DivideProblem

def parse(message):
	message = message.decode("utf-8")
	t, data = message.split(" ", 1)
	data = json.loads(data)
	if type(data) == dict:
		return Message.Types[t](**data)
	else:
		return Message.Types[t](*data)
