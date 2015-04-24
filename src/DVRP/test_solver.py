from parseVRP import *
from partitioning import *
from solver import *

vrp = VRP.CreateFromFile("okul12D.vrp")

nd = vrp.num_depots
for i in range(vrp.num_visits):
    if vrp.times[i+nd] > vrp.end * vrp.cutoff:
        vrp.times[i+nd] = 0
#print(vrp)
#
#c = 0; k = 7000
#for route in PartitionProblem(vrp, 10, 0):
#    c+=1
#    if(c % k == 0):
#        print(route)
#print(c)


routes = [
          [[1, 7, 12], [2, 5, 10], [3, 8], [4, 6, 9], [11]],
          [[1, 3], [2, 10], [4, 6, 8], [5, 11], [7], [9, 12]],
          [[1, 5, 7], [2, 9], [3, 11], [4, 6], [8, 12], [10]],
          [[1, 2, 7], [3, 10], [4, 12], [5, 8], [6, 9], [11]],
          [[1, 4, 12], [2, 6, 9], [3, 7], [5, 8], [10], [11]],
          [[1], [2, 6, 9], [3, 10], [4, 11], [5, 7], [8], [12]],
          [[1, 7], [2], [3], [4, 11], [5, 6], [8, 12], [9, 10]],
          [[1, 9], [2], [3], [4, 7, 12], [5, 11], [6, 10], [8]],
          [[1, 5], [2, 12], [3, 10], [4, 7], [6, 8], [9], [11]],
          [[1], [2, 11], [3, 6], [4, 7], [5], [8], [9], [10, 12]],
          [[1], [2, 9], [3, 10], [4, 7], [5], [6], [8], [11], [12]],
    [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12]]
    ]

minL = 5000
minsol=[]
for route in PartitionProblem(vrp, 2000, 5):
    sol = SolvePartialProblem(vrp, route)
    if(sol[0] != -1):
        if(sol[0] < minL):
            minL = sol[0]
            minsol = sol[1]

print([minL, minsol])

    
