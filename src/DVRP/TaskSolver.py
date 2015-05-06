from DVRP.parseVRP import *
from DVRP.partitioning import *
from DVRP.solver import *
import json

class TaskSolver:

    Name = "io.15.pl.15.DVRP"

    def __init__(self, common_data):
        self.vrp = VRP(common_data)

# thread_count: int # Number of threads in the whole cluster
    def divide(self, thread_count):
        partialProblems = []
        for i in range(thread_count):
            partialProblems.insert(i, PartitionProblem(self.vrp, thread_count, i))
        return partialProblems
        
# partial_data: bytes # Partial solutions / suboptimal solutions
# timeout: int # Partial solutions / suboptimal solutions
    def solve(self, partial_data, timeout):
        P = json.loads(partial_data)

        minL = 1000000
        minsol = []
        for route in P:
            sol = SolvePartialProblem(vrp, route)
            if(sol[0] > 0):
                if(sol[0] < minL):
                    minL = sol[0]
                    minsol = sol[1]
        return [minL, minsol]

# solutions: bytes[] # Partial solutions / suboptimal solutions
    def merge(self, solutions):
        minL = solutions[0][0]
        minsol = []
        for sol in solutions:
            if(sol[0] > 0):
                if(sol[0] < minL):
                    minL = sol[0]
                    minsol = sol[1]
        return [minL, minsol]
