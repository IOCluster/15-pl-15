class Signal:
	def __init__(self):
		self.q = []

	def queue(self, f):
		self.q.append(f)

	def notify(self):
		self.q.pop(0)()

	def notify_all(self):
		for f in self.q:
			f()
		self.q = []
