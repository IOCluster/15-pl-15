import threading
from iocluster import messages

class Problems:
	list = []
	lock = threading.Lock()

	def add(self, msg):
		self.lock.acquire()
		try:
			msg.Id = len(self.list)
			problem = Problem(msg)
			self.list.append(problem)
		finally:
			self.lock.release()
		return msg.Id

	def pendingForDivision(self):
		return [problem for problem in self.list if problem.status == Problem.New]

	def pendingForComputation(self):
		return [problem for problem in self.list if problem.status == Problem.Divided]

	def pendingForMerge(self):
		return [problem for problem in self.list if problem.status == Problem.Computed]

	def unassignedForDivision(self):
		return [problem for problem in self.pendingForDivision() if problem.componentId == None]

	def unassignedForComputation(self):
		return [problem for problem in self.pendingForComputation() if problem.componentId == None]

	def unassignedForMerge(self):
		return [problem for problem in self.pendingForMerge() if problem.componentId == None]

	def finished(self):
		return [problem for problem in self.list if problem.status == Problem.Done]

	def release(self, componentId):
		for problem in self.list:
			if problem.componentId == componentId: problem.componentId = None
			for task in problem.tasks.list:
				if task.componentId == componentId: task.componentId = None

problems = Problems()

class Problem:
	# New -> Look for TM to divide it
	New = 0
	# Divided -> Look for CNs to solve it
	Divided = 1
	# Computed -> Have all partial solutions, look for TM to merge it
	Computed = 2
	# Done -> Complete solution available
	Done = 3

	def __init__(self, msg):
		self.Id = msg.Id
		self.ProblemType = msg.ProblemType
		self.SolvingTimeout = msg.SolvingTimeout
		self.ProblemData = msg.Data
		self.SolutionData = ""
		self.CommonData = ""
		self.TimeoutOccured = False
		self.SolutionType = ""
		self.status = Problem.New
		self.registerMessage = msg
		self.ComputationsTime = 0
		self.componentId = None
		self.lock = threading.Lock()
		self.tasks = Tasks(self)

	def assignToComponent(self, id):
		self.lock.acquire()
		try:
			if self.componentId == None:
				self.componentId = id
				return True
			return False
		finally:
			self.lock.release()

	def updateWithDivide(self, msg):
		self.tasks.add(msg)
		self.CommonData = msg.CommonData
		self.status = Problem.Divided
		self.componentId = None
		print("* Problem #{:d} -> Divided into {:d} tasks".format(self.Id, len(self.tasks.list)))

	def updateWithSolutions(self, msg):
		# Partial solutions
		if self.status == Problem.Divided:
			for solution in msg.Solutions:
				task = self.tasks.list[solution.TaskId]
				task.updateWithSolution(solution)
			print("* Problem #{:d} -> Computed {:d}/{:d}".format(self.Id, len(self.tasks.list) - len(self.tasks.pending()), len(self.tasks.list)))
			if not self.tasks.pending():
				self.status = Problem.Computed
				print("* Problem #{:d} -> Computed All".format(self.Id))
		# Merged final solution
		elif self.status == Problem.Computed:
			solution = msg.Solutions[0]
			self.SolutionData = solution.Data
			self.ComputationsTime = solution.ComputationsTime
			self.SolutionType = solution.Type
			self.TimeoutOccured = solution.TimeoutOccured
			self.status = Problem.Done
			print("* Problem #{:d} -> Done".format(self.Id))

	def getComputationType(self):
		if self.status == Problem.Done:
			return self.SolutionType
		return "Ongoing"

	def getOngoingComputationsTime(self):
		return sum(task.ComputationsTime for task in self.tasks.list)

	def getSolutionRequestMessage(self):
		if self.status == Problem.Done:
			solutions = [{
				'ComputationsTime': self.ComputationsTime,
				'Type': self.SolutionType,
				'Data': self.SolutionData
			}]
			if self.TimeoutOccured:
				solutions[0]['TimeoutOccured'] = True
		else:
			solutions = [{
				'ComputationsTime': self.getOngoingComputationsTime(),
				'Type': 'Ongoing'
			}]
		return messages.Solutions(self.Id, self.ProblemType, solutions, self.CommonData)

class Tasks:
	def __init__(self, problem):
		self.list = []
		self.lock = threading.Lock()
		self.problem = problem

	def add(self, msg):
		self.lock.acquire()
		try:
			for partialProblem in msg.PartialProblems:
				task = Task(self.problem, partialProblem)
				self.list.append(task)
		finally:
			self.lock.release()

	def pending(self):
		return [task for task in self.list if task.status == Task.New]

	def unassigned(self):
		return [task for task in self.pending() if task.componentId == None]

	def areAllComputed(self):
		return sum(1 for task in self.list if task.status == Task.Computed) == len(self.list)

class Task: # AKA PartialProblem
	# New -> Look for CN to compute this partial problem
	New = 0
	# Computed -> Merge if all computed
	Computed = 1

	def __init__(self, problem, msg):
		self.problem = problem
		self.Id = msg.TaskId
		self.ProblemData = msg.Data
		self.NodeID = msg.NodeID
		self.TimeoutOccured = False
		self.SolutionType = ""
		self.SolutionData = ""
		self.ComputationsTime = 0
		self.status = Task.New
		self.componentId = None
		self.lock = threading.Lock()

	def assignToComponent(self, id):
		self.lock.acquire()
		try:
			if self.componentId == None:
				self.componentId = id
				return True
			return False
		finally:
			self.lock.release()

	def setComputed(self):
		self.lock.acquire()
		try:
			self.status = Task.Computed
			self.componentId = None
		finally:
			self.lock.release()

	def updateWithSolution(self, msg):
		self.TimeoutOccured = msg.TimeoutOccured
		self.SolutionType = msg.Type
		self.ComputationsTime = msg.ComputationsTime
		self.SolutionData = msg.Data
		self.setComputed()

