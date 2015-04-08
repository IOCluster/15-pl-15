from .serializer import Serializer
from .deserializer import Deserializer
import xml.etree.ElementTree as ET
import xml.dom.minidom

def prettify(dom):
	try:
		dom.documentElement.removeAttribute("xsi:noNamespaceSchemaLocation")
		dom.documentElement.removeAttribute("xmlns:xsi")
	except:
		pass
	x = dom.toprettyxml()
	out = ""
	for line in x.split('\n'):
		if line.strip():
			out += line + '\n'
	return out

def read_example_xml(msg_type):
	example_xml = open('UCC_2015/xml/' + msg_type + '.xml').read()
	out = ""
	for line in example_xml.split("\n"):
		out += line.strip() + "\n"
	return out

def test_serialize(msg_type, data):
	example_xml = read_example_xml(msg_type)
	orig = xml.dom.minidom.parseString(example_xml)
	ser = Serializer("UCC_2015/xml/" + msg_type + ".xsd")
	our = xml.dom.minidom.parseString(ser(data))

	if prettify(orig) == prettify(our):
		print(msg_type + " OK")
		return

	print(prettify(orig))
	print(prettify(our))

def test_deserialize(msg_type, data):
	read_data = Deserializer("UCC_2015/xml/" + msg_type + ".xsd")(read_example_xml(msg_type))

	if data == read_data:
		print(msg_type + " OK")
		return

	print(data)
	print(read_data)

def test(msg_type, data):
	test_serialize(msg_type, data)
	test_deserialize(msg_type, data)

data = "SWRlYWx5IHNhIGphayBnd2lhemR5IC0gbmllIG1vem5hIGljaCBvc2lhZ25hYywgYWxlIG1v\nem5hIHNpZSBuaW1pIGtpZXJvd2FjLg0K"
n_data_n = "\n" + data + "\n"

test("DivideProblem", dict(ProblemType="TSP", Id=12, Data=data, ComputationalNodes=16, NodeID=8))

test("NoOperation", dict(BackupCommunicationServers=[dict(address="192.168.100.1", port=65535)]))

test("PartialProblems", dict(ProblemType="TSP", Id=12, CommonData=n_data_n, PartialProblems=[dict(TaskId=1, Data=n_data_n, NodeID=7), dict(TaskId=2, Data=n_data_n, NodeID=3), dict(TaskId=3, Data=n_data_n, NodeID=7), dict(TaskId=4, Data=n_data_n, NodeID=15)]))

test("Register", dict(Type="TaskManager", SolvableProblems=["TSP", "3-SAT", "DVRP", "GraphColoring"], ParallelThreads=8, Deregister=False, Id=12))

test("RegisterResponse", dict(Id=12, Timeout=120, BackupCommunicationServers=[dict(address="192.168.100.1", port=65535)]))

test("Solution", dict(ProblemType="TSP", Id=12, CommonData=n_data_n, Solutions=[dict(TaskId=123, TimeoutOccured=False, Type="Final", ComputationsTime=12334, Data=n_data_n)]))

test("SolveRequest", dict(ProblemType="TSP", SolvingTimeout=3600000, Data=data, Id=12))

test("SolveRequestResponse", dict(Id=12))

test("Status", dict(Id=12, Threads=[dict(State="Idle"), dict(State="Idle"), dict(State="Busy", HowLong=1244656, ProblemInstanceId=1212, TaskId=123, ProblemType="TSP")]))
