import threading
from iocluster import messages
from iocluster.util import current_time_ms
from iocluster.master.problem import problems, Problem

# All components: CN, TM, BCS
class Components:
	list = []
	lock = threading.Lock()

	def add(self, msg):
		self.lock.acquire()
		try:
			msg.Id = len(self.list)
			component = Component.Types[msg.Type](msg)
			self.list.append(component)
		finally:
			self.lock.release()
		return msg.Id

	def active(self):
		return [component for component in self.list if not component.dead]

	def ComputationalNodes(self):
		return [component for component in self.active() if component.type == Component.ComputationalNode]

	def getThreadCount(self):
		return sum(component.threads for component in self.ComputationalNodes())

components = Components()

class Component:
	Types = dict()
	TaskManager = "TaskManager"
	ComputationalNode = "ComputationalNode"
	CommunicationServer = "CommunicationServer"

	def __init__(self, msg):
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
	def __init__(self, msg):
		Component.__init__(self, msg)
		self.type = Component.TaskManager
		self.problems = msg.SolvableProblems
		self.threads = msg.ParallelThreads

	def parseStatus(self, msg):
		pass

	def chooseProblem(self):
		# Find suitable problem and try to assign component
		available = problems.unassignedForMerge() + problems.unassignedForDivision()
		print("TM available: {:s}".format(str(["#{:d}".format(x.Id) for x in available])))
		# Avoid race condition when assigning the same unassigned component at one time by two threads
		for problem in available:
			if problem.assignToComponent(self.id):
				return problem
		return None

	def sendNoOperationMessage(self, conn):
		response = messages.NoOperation([])
		conn.send(response)

	def sendDivideMessage(self, conn, problem):
		response = messages.DivideProblem(problem.Id, problem.ProblemType, problem.ProblemData, components.getThreadCount(), self.id)
		conn.send(response)

	def sendSolutionsMessage(self, conn, problem):
		solutions = []
		for task in problem.tasks.list:
			solutions.append({
				"TaskId": task.Id,
				"Type": task.SolutionType,
				"ComputationsTime": task.ComputationsTime,
				"Data": task.SolutionData,
				"TimeoutOccured": task.TimeoutOccured
			})
		response = messages.Solutions(problem.Id, problem.ProblemType, solutions)
		conn.send(response)

	def sendMessages(self, conn):
		self.sendNoOperationMessage(conn)

		assignedProblem = self.chooseProblem()
		print("TM assigned: #{:d}".format(assignedProblem.Id) if assignedProblem != None else "TM assigned: None")
		if assignedProblem != None:
			if assignedProblem.status == Problem.New:
				self.sendDivideMessage(conn, assignedProblem)
			elif assignedProblem.status == Problem.Computed:
				self.sendSolutionsMessage(conn, assignedProblem)
		

Component.Types["TaskManager"] = TaskManager

class ComputationalNode(Component):
	def __init__(self, msg):
		Component.__init__(self, msg)
		self.type = Component.ComputationalNode
		self.problems = msg.SolvableProblems
		self.threads = msg.ParallelThreads

	def solve(self, task):
		pass

	def parseStatus(self, msg):
		pass

	def sendMessages(self, conn):
		# Find suitable task and try to assign component
		available = [task for problem in problems.unassignedForComputation() for task in problem.tasks.unassigned()]
		print("CN available: {:s}".format(str(["#{:d}".format(x.Id) for x in available])))
		assignedTask = None
		for task in available:
			if task.assignToComponent(self.id):
				assignedTask = task
				break

		print("CN assigned: #{:d}".format(assignedTask.Id) if assignedTask != None else "CN assigned: None")

		# Send NoOperation with backup servers list
		response = messages.NoOperation([])
		conn.send(response)

		# Send PartialProblem to compute if pending
		if assignedTask != None:
			partialProblems = []
			partialProblem = {
				"TaskId": assignedTask.Id,
				"Data": assignedTask.ProblemData,
				"NodeID": assignedTask.NodeID
			}
			partialProblems.append(partialProblem)
			response = messages.SolvePartialProblems(assignedTask.problem.Id, assignedTask.problem.ProblemType, assignedTask.problem.CommonData, partialProblems)
			conn.send(response)

Component.Types["ComputationalNode"] = ComputationalNode

class CommunicationServer(Component):
	def __init__(self, msg):
		Component.__init__(self, msg)
		self.type = Component.CommunicationServer

	def synchronize(self):
		pass

	def parseStatus(self, msg):
		pass

	def sendMessages(self, conn):
		response = messages.NoOperation([])
		conn.send(response)

Component.Types["CommunicationServer"] = CommunicationServer
