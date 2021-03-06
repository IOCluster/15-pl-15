from partitioning import *

A = range(6)

print("Wszystkie podzialy zbioru [1,2,3,4,5,6] o licznosci 6")
pretty_print(algorithm_u(A,4))

print("\n\n")
print("Partition dla n_depots = 2, n_nodes = 4, n_visits = 5, nodeId = 1" )
n_depots = 2
n_nodes = 4
n_visits = 5
which_node = 1
print(list(Partition(n_nodes, n_depots, n_visits, which_node)))

print("\n")
print("Partition dla n_depots = 1, n_nodes = 3, n_visits = 4" )
for i in range(3):
    for i in Partition(3, 1, 4, i):
        print(i)
    print("\n")

print("Partition dla okul12D, num_node = 10, nodeID=0")
import parseVRP
vrp = parseVRP.VRP.CreateFromFile("okul12D.vrp")
print(len(list(Partition(10, vrp.num_depots, vrp.num_visits, 0))))
    
print("PartialProblem dla okul12D, num_node = 10, nodeID=0")
import parseVRP
vrp = parseVRP.VRP.CreateFromFile("okul12D.vrp")
print(len(list(PartitionProblem(vrp, 10, 0))))
