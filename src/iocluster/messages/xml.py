from argparse import Namespace
from iocluster import xml
import xml.etree.ElementTree as ET

xsds = {
	"DivideProblem": "DivideProblem.xsd",
	"NoOperation": "NoOperation.xsd",
	"SolvePartialProblems": "PartialProblems.xsd",
	"Register": "Register.xsd",
	"RegisterResponse": "RegisterResponse.xsd",
	"Solutions": "Solution.xsd",
	"SolutionRequest": "SolutionRequest.xsd",
	"SolveRequest": "SolveRequest.xsd",
	"SolveRequestResponse": "SolveRequestResponse.xsd",
	"Status": "Status.xsd"
}

def encode(o):
	if isinstance(o, Namespace):
		return o.__dict__
	return o

def dump(msg):
	msg_type = type(msg).__name__
	return xml.Serializer("UCC_2015/xml/" + xsds[msg_type], encode)(msg)

def parse(message):
	m = ET.fromstring(message)
	msg_type = m.tag.replace("{http://www.mini.pw.edu.pl/ucc/}", "")
	return msg_type, xml.Deserializer("UCC_2015/xml/" + xsds[msg_type])(message)
