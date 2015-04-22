from Partitioning import *

A = range(6)

pretty_print(algorithm_u(A,4))

print("\n\n")

n_depots = 2
n_nodes = 4
n_visits = 5
which_node = 1

pretty_print(PartitionProblem(n_nodes, n_depots, n_visits, which_node))

for i in range(3):
    for i in Partitioning.PartitionProblem(3, 1, 4, i):
        print(i)
    print("\n")



