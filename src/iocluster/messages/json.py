from argparse import Namespace
import json

class NamespaceEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Namespace):
			return o.__dict__

def dump(msg):
	return type(msg).__name__ + " " + json.dumps(msg.__dict__, cls=NamespaceEncoder)

def parse(message):
	t, data = message.split(" ", 1)
	data = json.loads(data)
	return t, data
