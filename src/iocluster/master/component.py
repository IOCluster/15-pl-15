from iocluster import messages
from iocluster.util import current_time_ms

class Component:
	Types = dict()

	def __init__(self, conn, msg):
		self.conn = conn
		self.dead = False
		self.id = msg.Id
		self.lastAlive = current_time_ms()
		self.problems = msg.SolvableProblems
		self.threads = msg.ParallelThreads
		self.registerMessage = msg

	# timeout in ms
	def isAlive(self, timeout):
		self.dead = current_time_ms() - self.lastAlive > timeout
		return not self.dead

	def touch(self):
		self.lastAlive = current_time_ms()

class TaskManager(Component):
	def DivideProblem(self, task, threads):
		self.conn.send(messages.DivideProblem(task.Id, task.ProblemType, task.Data, threads, self.id))

	def MergeSolution(self, task):
		pass

Component.Types["TaskManager"] = TaskManager

class ComputationalNode(Component):
	def Solve(self, task):
		pass

Component.Types["ComputationalNode"] = ComputationalNode
