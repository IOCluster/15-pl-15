
class TaskSolver:

	Name = "io.15.pl.15.DummyProblem"

	def __init__(self, common_data):
		self.common_data = int(common_data)

	# thread_count: int # Number of threads in the whole cluster
	def divide(self, thread_count):
		for i in range(6):
			yield i

	# partial_data: bytes # Partial solutions / suboptimal solutions
	# timeout: int # Partial solutions / suboptimal solutions
	def solve(self, partial_data, timeout):
		try:
			time.sleep(3)
		except:
			pass
		return int(partial_data) * self.common_data

	# solutions: bytes[] # Partial solutions / suboptimal solutions
	def merge(self, solutions):
		v = 0
		for solution in solutions:
			v += int(solution)

		try:
			time.sleep(3)
		except:
			pass

		return v
