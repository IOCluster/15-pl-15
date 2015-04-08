import xml.etree.ElementTree as ET

xs = "{http://www.w3.org/2001/XMLSchema}"

def cast(xml_text, xml_type=None):
	if not xml_type:
		return xml_text
	elif xml_type == "xs:boolean":
		return True if xml_text == "true" else False
	elif xml_type.startswith("xs:unsigned"):
		return int(xml_text)
	else:
		return xml_text

def deserialize(xml, el, ns):

	xml_text = xml.text if xml.text else None

	if "type" in el.attrib or el[0].tag == xs + "simpleType":
		return cast(xml_text, el.attrib["type"] if "type" in el.attrib else None)

	elif el[0].tag == xs + "complexType":

		attributes = [x for x in el[0] if x.tag == xs + "attribute"]
		other = [x for x in el[0] if x.tag != xs + "attribute"]

		data = dict()
		for attr in attributes:
			if attr.attrib["name"] in xml.attrib:
				data[attr.attrib["name"]] = cast(xml.attrib[attr.attrib["name"]], attr.attrib["type"] if "type" in attr.attrib else None)

		if len(other):
			if other[0].tag != xs + "sequence":
				print("ERROR: Only sequence complex types are supported.")

			seq = el[0][0]

			maxOccurs = seq[0].attrib.get("maxOccurs", "1")
			if maxOccurs == "1":
				# dict.
				for e in seq:
					matching_children = [child for child in xml if child.tag == "{" + ns + "}" + e.attrib["name"]]
					if len(matching_children) == 1:
						data[e.attrib["name"]] = deserialize(matching_children[0], e, ns)
					elif len(matching_children) == 0:
						# skip
						pass
					else:
						raise ValueError

			elif maxOccurs != "0":
				# list.
				data = []

				for child in xml:
					data.append(deserialize(child, seq[0], ns))

	else:
		print("ERROR: Expected type, got " + el[0].tag)

	return data

class Deserializer:
	def __init__(self, xsd):
		self.schema = ET.parse(xsd).getroot()

	def __call__(self, xml):
		return deserialize(ET.fromstring(xml), self.schema[0], self.schema.attrib["targetNamespace"])
