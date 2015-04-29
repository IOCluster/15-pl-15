from parseVRP import *

from partitioning import *
from solver import *

vrp = VRP.CreateFromFile("test.vrp")

nd = vrp.num_depots
for i in range(vrp.num_visits):
    if vrp.times[i+nd] > vrp.end * vrp.cutoff:
        vrp.times[i+nd] = 0

minL = 5000
minsol=[]
count = 0;
P = PartitionProblem(vrp, 1, 0)
print("_"*30)
for route in P:
    sol = SolvePartialProblem(vrp, route)
    count+=1
    if(count % 10000 ==0):
        print("|", end='')
    if(sol[0] > 0):
        if(sol[0] < minL):
            minL = sol[0]
            minsol = sol[1]
#        if(sol[0] < 800):
#            print([sol[0], sol[1]])

print([minL, minsol])
