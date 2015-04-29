
class TaskSolver:

	Name = "io.15.pl.15.DummyProblem"

	def __init__(self, common_data):
		...

	# thread_count: int # Number of threads in the whole cluster
	def divide(self, thread_count):
		...

	# partial_data: bytes # Partial solutions / suboptimal solutions
	# timeout: int # Partial solutions / suboptimal solutions
	def solve(self, partial_data, timeout):
		...

	# solutions: bytes[] # Partial solutions / suboptimal solutions
	def merge(self, solutions):
		...
