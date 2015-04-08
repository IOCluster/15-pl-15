import xml.etree.ElementTree as ET

xs = "{http://www.w3.org/2001/XMLSchema}"

def serialize(data, el, encoder=None, ns=None):

	if data is None:
		return ""

	if encoder:
		data = encoder(data)

	#print(el.attrib['name'], data)

	out = '<' + el.attrib['name'] + (' xmlns="' + ns + '"' if ns else "")

	if "type" in el.attrib or el[0].tag == xs + "simpleType":
		out += '>'

		if "type" in el.attrib and el.attrib["type"] == "xs:boolean":
			out += "true" if data else "false"
		else:
			out += str(data)

	elif el[0].tag == xs + "complexType":

		attributes = [x for x in el[0] if x.tag == xs + "attribute"]
		other = [x for x in el[0] if x.tag != xs + "attribute"]

		for attr in attributes:
			if attr.attrib["name"] in data:
				out += ' {}="{}"'.format(attr.attrib["name"], data[attr.attrib["name"]])

		out += '>'

		if len(other):
			if other[0].tag != xs + "sequence":
				print("ERROR: Only sequence complex types are supported.")

			seq = el[0][0]

			if type(data) == dict:

				for e in seq:
					if e.attrib["name"] in data:
						out += serialize(data[e.attrib["name"]], e, encoder)
					elif e.attrib.get("minOccurs", "1") != "0":
						raise ValueError

			elif type(data) == list:

				maxOccurs = seq[0].attrib.get("maxOccurs", "1")
				if maxOccurs != "unbounded" and int(maxOccurs) < len(data):
					raise ValueError

				for v in data:
					out += serialize(v, seq[0], encoder)

	else:
		print("ERROR: Expected type, got " + el[0].tag)

	out += '</' + el.attrib['name'] + '>'

	return out

class Serializer:
	def __init__(self, xsd, encoder=None):
		self.schema = ET.parse(xsd).getroot()
		self.encoder = encoder

	def __call__(self, data):
		return serialize(data, self.schema[0], self.encoder, ns=self.schema.attrib["targetNamespace"])
