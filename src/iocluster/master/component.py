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
		return sum(len(component.threads.list) for component in self.ComputationalNodes())

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
		self.solvableProblems = msg.SolvableProblems
		self.threads = ComponentThreads(msg.ParallelThreads)

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

	def parseStatus(self, msg):
		self.threads.updateWithState(msg)

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
		# Send tasks
		for i in range(self.threads.getAvailableCount()):
			assignedProblem = self.chooseProblem()
			if assignedProblem == None:
				if i == 0: print("TM assigned: None")
				break
			print("TM assigned: #{:d}".format(assignedProblem.Id))
			if assignedProblem.status == Problem.New:
				self.sendDivideMessage(conn, assignedProblem)
			elif assignedProblem.status == Problem.Computed:
				self.sendSolutionsMessage(conn, assignedProblem)

Component.Types["TaskManager"] = TaskManager

class ComputationalNode(Component):
	def __init__(self, msg):
		Component.__init__(self, msg)
		self.type = Component.ComputationalNode

	def parseStatus(self, msg):
		self.threads.updateWithState(msg)

	def chooseProblem(self):
		# Find suitable task and try to assign component
		available = [task for problem in problems.unassignedForComputation() for task in problem.tasks.unassigned()]
		print("CN available: {:s}".format(str(["#{:d}".format(x.Id) for x in available])))
		for task in available:
			if task.assignToComponent(self.id):
				return task

	def sendNoOperationMessage(self, conn):
		response = messages.NoOperation([])
		conn.send(response)

	def sendSolvePartialProblemsMessage(self, conn, assignedTasks):
		# Find different problems
		problems = []
		for assignedTask in assignedTasks:
			problem = assignedTask.problem
			if not problem in problems: problems.append(problem)
		# Send message for each problem
		for problem in problems:
			partialProblems = []
			for assignedTask in assignedTasks:
				if assignedTask.problem == problem:
					partialProblems.append({
						"TaskId": assignedTask.Id,
						"Data": assignedTask.ProblemData,
						"NodeID": assignedTask.NodeID
					})
			response = messages.SolvePartialProblems(problem.Id, problem.ProblemType, problem.CommonData, partialProblems)
			conn.send(response)

	def sendMessages(self, conn):
		self.sendNoOperationMessage(conn)
		# Send PartialProblem to compute if pending
		assignedTasks = []
		for i in range(self.threads.getAvailableCount()):
			assignedTask = self.chooseProblem()
			if assignedTask == None:
				if i == 0: print("CN assigned: None")
				break
			print("CN assigned: #{:d}".format(assignedTask.Id))
			assignedTasks.append(assignedTask)
		self.sendSolvePartialProblemsMessage(conn, assignedTasks)

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

class ComponentThreads:
	def __init__(self, count):
		self.list = []
		for i in range(count):
			thread = ComponentThread()
			self.list.append(thread)

	def updateWithState(self, msg):
		newList = []
		for threadMsg in msg.Threads:
			thread = ComponentThread(threadMsg)
			newList.append(thread)
		self.list = newList

	def getAvailableCount(self):
		return sum(1 for thread in self.list if thread.State == "Idle")

class ComponentThread:
	def __init__(self, msg=None):
		if msg == None:
			self.State = "Idle"
			self.HowLong = None
			self.ProblemInstanceId = None
			self.TaskId = None
			self.ProblemType = None
		else:
			self.State = msg.State
			self.HowLong = msg.HowLong if msg.HowLong else None
			self.ProblemInstanceId = msg.ProblemInstanceId if msg.ProblemInstanceId else None
			self.TaskId = msg.TaskId if msg.TaskId else None
			self.ProblemType = msg.ProblemType if msg.ProblemType else None
