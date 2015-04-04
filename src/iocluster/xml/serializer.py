import xml.etree.ElementTree as ET

xs = "{http://www.w3.org/2001/XMLSchema}"

def serialize(data, el, ns=None):

	if data is None:
		return ""

	out = '<' + el.attrib['name'] + (' xmlns="' + ns + '"' if ns else "") + '>'

	if "type" in el.attrib or el[0].tag == xs + "simpleType":
		if "type" in el.attrib and el.attrib["type"] == "xs:boolean":
			out += "true" if data else "false"
		else:
			out += str(data)

	elif el[0].tag == xs + "complexType":

		if el[0][0].tag != xs + "sequence":
			print("ERROR: Only sequence complex types are supported.")

		seq = el[0][0]

		if type(data) == dict:

			for e in seq:
				if e.attrib["name"] in data:
					out += serialize(data[e.attrib["name"]], e)
				elif e.attrib.get("minOccurs", "1") != "0":
					raise ValueError

		elif type(data) == list:

			if seq[0].attrib.get("maxOccurs", "1") != "unbounded":
				raise ValueError

			for v in data:
				out += serialize(v, seq[0])

	else:
		print("ERROR: Expected type, got " + el[0].tag)

	out += '</' + el.attrib['name'] + '>'

	return out

class Serializer:
	def __init__(self, xsd):
		self.schema = ET.parse(xsd).getroot()

	def __call__(self, data):
		return serialize(data, self.schema[0], self.schema.attrib["targetNamespace"])
