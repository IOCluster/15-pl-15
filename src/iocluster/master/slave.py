class Slave:
	Types = dict()

	def __init__(self, conn, problems, threads):
		self.conn = conn
		self.problems = problems
		self.threads = threads

class TaskManager(Slave):
	methods = ["DivideProblem", "MergeSolution"]
Slave.Types["TaskManager"] = TaskManager

class ComputationalNode(Slave):
	methods = ["Solve"]
Slave.Types["ComputationalNode"] = ComputationalNode
