from DVRP.parseVRP import *
from DVRP.partitioning import *
from DVRP.solver import *
import json

class TaskSolver:

    Name = "io.15.pl.15.DVRP"

    def __init__(self, common_data):
        vrp = VRP(common_data)
        nd = vrp.num_depots
        for i in range(vrp.num_visits):
            if(vrp.times[i+nd] > vrp.cutoff * vrp.end):
                vrp.times[i+nd] = 0
        self.vrp = vrp
        

# thread_count: int # Number of threads in the whole cluster
    def divide(self, thread_count):
        partialProblems = []
        for i in range(thread_count):
            partialProblems.insert(i,list( PartitionProblem(self.vrp, thread_count, i)))
        return partialProblems
        
# partial_data: bytes # Partial solutions / suboptimal solutions
# timeout: int # Partial solutions / suboptimal solutions
    def solve(self, partial_data, timeout):
        P = json.loads(partial_data)
        minL = 100000
        minsol = []
        for route in P:
            sol = SolvePartialProblem(self.vrp, route)
            if(sol[0] > 0):
                if(sol[0] < minL):
                    minL = sol[0]
                    minsol = sol[1]
        return [minL, minsol]

# solutions: bytes[] # Partial solutions / suboptimal solutions
    def merge(self, solutions):
        sol1 = json.loads(solutions[0])
        minL = sol1[0]
        minsol = []
        for sol in solutions:
            psol = json.loads(sol)
            L = psol[0]
            if(L > 0):
                if(L < minL):
                    minL = L
                    minsol = psol[1]
        return [minL, minsol]
