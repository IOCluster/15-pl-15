from parseVRP import Point

def SolvePartialProblem(vrp, sol):
    depots = range(vrp.num_depots)
    visits = range(vrp.num_visits)
    depots_loc = [vrp.location_coords[vrp.locations[i]] for i in depots]
    visits_loc = [vrp.location_coords[vrp.locations[i]] for i in range(vrp.num_depots, vrp.num_locations)]

    dist = [[visits_loc[i].Distance(visits_loc[j]) for i in visits] for j in visits]
    dep_dist = [[visits_loc[i].Distance(depots_loc[j]) for i in visits] for j in depots]
                  
#dep_dist[dep][vis]
