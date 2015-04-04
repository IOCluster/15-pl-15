import threading
from iocluster import messages
from iocluster.util import current_time_ms
from iocluster.master.task import tasks

# All components: CN, TM, BCS
class Components:
	list = []
	lock = threading.Lock()

	def add(self, conn, msg):
		self.lock.acquire()
		try:
			msg.Id = len(self.list)
			component = Component.Types[msg.Type](conn, msg)
			self.list.append(component)
		finally:
			self.lock.release()
		return msg.Id

components = Components()

class Component:
	Types = dict()

	def __init__(self, conn, msg):
		self.conn = conn
		self.dead = False
		self.id = msg.Id
		self.lastAlive = current_time_ms()
		self.registerMessage = msg

	# timeout in ms
	def isAlive(self, timeout):
		self.dead = current_time_ms() - self.lastAlive > timeout
		return not self.dead

	def touch(self):
		self.lastAlive = current_time_ms()

class TaskManager(Component):
	def __init__(self, conn, msg):
		Component.__init__(self, conn, msg)
		self.problems = msg.SolvableProblems
		self.threads = msg.ParallelThreads

	def divideProblem(self, task, threads):
		self.conn.send(messages.DivideProblem(task.Id, task.ProblemType, task.Data, threads, self.id))

	def mergeSolution(self, task):
		pass

	def parseStatus(self, msg):
		pass

	def sendMessages(self, conn):
		response = messages.NoOperation([])
		conn.send(response)

Component.Types["TaskManager"] = TaskManager

class ComputationalNode(Component):
	def solve(self, task):
		pass

	def parseStatus(self, msg):
		pass

	def sendMessages(self, conn):
		response = messages.NoOperation([])
		conn.send(response)

Component.Types["ComputationalNode"] = ComputationalNode

class CommunicationServer(Component):
	def synchronize(self):
		pass

	def parseStatus(self, msg):
		pass

	def sendMessages(self, conn):
		response = messages.NoOperation([])
		conn.send(response)

Component.Types["CommunicationServer"] = CommunicationServer
