from iocluster import messages
from iocluster.master.signal import Signal

class Slave:
	Types = dict()

	def __init__(self, id, conn, problems, threads):
		self.id = id
		self.conn = conn
		self.problems = problems
		self.threads = threads
		self.died = Signal()

class TaskManager(Slave):
	def DivideProblem(self, task, threads):
		self.conn.send(messages.DivideProblem(task.Id, task.ProblemType, task.Data, threads, self.id))

	def MergeSolution(self, task):
		...

Slave.Types["TaskManager"] = TaskManager

class ComputationalNode(Slave):
	def Solve(self, task):
		...

Slave.Types["ComputationalNode"] = ComputationalNode
