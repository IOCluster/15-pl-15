from iocluster.messages import xml as transport

from argparse import Namespace
import socket as sys_socket

DEBUG_MESSAGES = False

SEPARATOR = b"\x17"	# == ctrl+w
# SEPARATOR = b"\n"

class Connection:
	def __init__(self, socket, timeout=None):
		self.buffer = b""
		self.socket = socket
		self.socket.setsockopt(sys_socket.SOL_SOCKET, sys_socket.SO_REUSEADDR, 1)
		if timeout:
			self.socket.settimeout(timeout)

	def send(self, message):
		self.socket.send(message + SEPARATOR)

	# Iterate over messages separated by SEPARATOR, break after recv 0 bytes
	def __iter__(self):
		while True:
			data = self.socket.recv(8192)
			if not data:
				if self.buffer:
					yield parse(self.buffer)
				break
			self.buffer += data
			while SEPARATOR in self.buffer:
				yield parse(self.buffer[:self.buffer.find(SEPARATOR)])
				self.buffer = self.buffer[self.buffer.find(SEPARATOR) + 1:]

class Message(Namespace):
	Types = dict()

	def __str__(self):
		d = transport.dump(self)
		if DEBUG_MESSAGES:
			print("OUTGOING MESSAGE --------------------")
			print(Namespace.__str__(self))
			print("--------------------")
			print(d)
		return d

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
		Threads = [x if isinstance(x, Thread) else Thread(**x) for x in Threads]
		Namespace.__init__(self, Id=Id, Threads=Threads)
Message.Types["Status"] = Status

class Thread(Message):
	def __init__(self, State, HowLong=None, ProblemInstanceId=None, TaskId=None, ProblemType=None):
		Namespace.__init__(self, State=State, HowLong=HowLong, ProblemInstanceId=ProblemInstanceId, TaskId=TaskId, ProblemType=ProblemType)

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
	def __init__(self, Id, ProblemType, Solutions, CommonData=None):
		Solutions = [x if isinstance(x, Solution) else Solution(**x) for x in Solutions]
		Namespace.__init__(self, ProblemType=ProblemType, Id=Id, CommonData=CommonData, Solutions=Solutions)
Message.Types["Solutions"] = Solutions

class DivideProblem(Message):
	def __init__(self, Id, ProblemType, Data, ComputationalNodes, NodeID):
		Namespace.__init__(self, ProblemType=ProblemType, Id=Id, Data=Data, ComputationalNodes=ComputationalNodes, NodeID=NodeID)
Message.Types["DivideProblem"] = DivideProblem

class PartialProblem(Namespace):
	def __init__(self, TaskId, Data, NodeID):
		Namespace.__init__(self, TaskId=TaskId, Data=Data, NodeID=NodeID)

class SolvePartialProblems(Message):
	def __init__(self, Id, ProblemType, CommonData, PartialProblems, SolvingTimeout=None):
		PartialProblems = [x if isinstance(x, PartialProblem) else PartialProblem(**x) for x in PartialProblems]
		Namespace.__init__(self, ProblemType=ProblemType, Id=Id, CommonData=CommonData, SolvingTimeout=SolvingTimeout, PartialProblems=PartialProblems)
Message.Types["SolvePartialProblems"] = SolvePartialProblems

def parse(message):
	message = message.decode("utf-8")
	t, data = transport.parse(message)
	if DEBUG_MESSAGES:
		print("INCOMING MESSAGE --------------------")
		print(message)
		print("--------------------")
		print(t, data)
	if type(data) == dict:
		return Message.Types[t](**data)
	else:
		return Message.Types[t](*data)
