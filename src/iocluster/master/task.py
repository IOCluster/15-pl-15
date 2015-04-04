import threading
from iocluster import messages

# All tasks: Problem, Partial Problem, Partial Solution, Solution
class Tasks:
	list = []
	lock = threading.Lock()

	def add(self, msg):
		self.lock.acquire()
		try:
			msg.Id = len(self.list)
			task = Task(msg)
			self.list.append(task)
		finally:
			self.lock.release()
		return msg.Id

tasks = Tasks()

class Task:
	# New -> Look for TM to divide it
	New = 0
	# Divided -> Look for CNs to solve it
	Divided = 1
	# Merging -> Have all partial solutions, look for TM to merge it
	Merging = 2
	# Done -> Complete solution available
	Done = 3

	def __init__(self, msg):
		self.Id = msg.Id
		self.ProblemType = msg.ProblemType
		self.SolvingTimeout = msg.SolvingTimeout
		self.ProblemData = msg.Data
		self.status = Task.New
		self.registerMessage = msg
		self.computationsTime = 0
		self.CommonData = ""

	def getSolutionRequestMessage(self):
		if self.status == Task.New or self.status == Task.Divided or self.status == Task.Merging:
			solutions = [{
				'ComputationsTime': self.computationsTime,
				'Type': 'Ongoing'
			}]
		elif self.status == Task.Done:
			if self.timeoutOccured:
				solutions = [{
					'ComputationsTime': self.computationsTime,
					'Type': 'Partial',
					'Data': 'TODO',
					'TimeoutOccured': True
				}]
			else:
				solutions = [{
					'ComputationsTime': self.computationsTime,
					'Type': 'Final',
					'Data': 'TODO'
				}]
		return messages.Solutions(self.Id, self.ProblemType, solutions)
