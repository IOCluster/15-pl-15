from .serializer import Serializer
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

def test(msg_type, data):
	orig = xml.dom.minidom.parse('UCC_2015/xml/' + msg_type + '.xml')
	ser = Serializer("UCC_2015/xml/" + msg_type + ".xsd")
	our = xml.dom.minidom.parseString(ser(data))

	if prettify(orig) == prettify(our):
		print(msg_type + " OK")
		return

	print(prettify(orig))
	print(prettify(our))

test("Status", dict(Id=12, Threads=[dict(State="Idle"), dict(State="Idle"), dict(State="Busy", HowLong=1244656, ProblemInstanceId=1212, TaskId=123, ProblemType="TSP")]))

test("Register", dict(Type="TaskManager", SolvableProblems=["TSP", "3-SAT", "DVRP", "GraphColoring"], ParallelThreads=8, Deregister=False, Id=12))
