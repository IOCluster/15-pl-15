from DVRP.parseVRP import Point
from itertools import permutations

def SolvePartialProblem(vrp, route):
    depots = range(vrp.num_depots)
    visits = range(vrp.num_visits)
    depots_loc = [vrp.location_coords[vrp.locations[i]] for i in depots]
    visits_loc = [vrp.location_coords[vrp.locations[i]] for i in range(vrp.num_depots, vrp.num_locations)]
    times = [vrp.times[i] for i in range(vrp.num_depots, vrp.num_locations)]
    dur = [vrp.durations[i] for i in visits]
    dist = [[visits_loc[i].Distance(visits_loc[j]) for i in visits] for j in visits]
    dep_dist = [[visits_loc[i].Distance(depots_loc[j]) for j in depots] for i in visits]

    #Znajdujemy zgrubne oszacowanie na dlugosc drogi - liczba wizyt * najdluzsza droga z i do hurtowni
    max_dist = max([max(l) for l in dist])
    max_dep_dist = max([max(l) for l in dep_dist])

    max_route = vrp.num_visits*max_dep_dist*2

    if(len(route) > vrp.num_vehicles):
        #TODO
        

    R = []
    L = 0
#Dla kazdego kawalka drogi sprawdzamy wszystkie permutacje wierzcholkow
#czy ktoras jest poprawnym rozwiazaniem
    for sub in route:
        part_min = max_route
        part_R = []
        for s in permutations(sub):
            q = [i-vrp.num_depots for i in s]
            #dolne oszacowanie na dlugosc danej sciezki
            up_L = min(dep_dist[q[0]]) + sum([ dist[q[i]][q[i+1]] for i in range(len(q)-1) ]) + min(dep_dist[q[-1]])
            #jesli jest dluzsza od juz znalezionego min, to nie spr
            if(up_L > part_min):
                continue

            #obliczamy czasy przyjazdu
            arv = []
            #znajdujemy najblizszy depot dla punktu startowego
            val0 =  min(dep_dist[q[0]])
            dep0 =  dep_dist[q[0]].index(val0)
            val0 += times[q[0]]
            arv.insert(0, val0)
            #i obliczamy arv dla dalszych zamowien
            for i in range(1,len(q)):
                val = max(times[q[i]] + dist[q[i]][q[i-1]], arv[i-1] + dur[q[i-1]] + dist[q[i]][q[i-1]])
                arv.insert(i, val)

            #teraz szukamy depot, do ktorego jestesmy w stanie wrocic
                          #przed zamknieciem i wracamy do najblizszego
            #jesli nie ma takiego, to przechodzimy do nastepnego przypadku
            valN = max(dep_dist[q[-1]])+1
            depN =  -1
            for i in range(vrp.num_depots):
                if(arv[-1]+dep_dist[q[-1]][i] <= vrp.times[i]['end']):
                    if(dep_dist[q[-1]][i] < valN):
                        depN=i
                        valN = dep_dist[q[-1]][i]
            if(depN == -1):
                #nie znalezlismy dobrego depotu
                continue
            
            #rozpatrywana permutacja spelnia ograniczenia
            #jesli jest lepsza od minimum, to
            #zapisujemy ja i dlugosc drogi
            part_L = val0 + sum([ dist[q[i]][q[i+1]] for i in range(len(q)-1) ]) + valN
            if(part_min > part_L):
                part_R = []
                part_R.append(dep0)
                for p in s:
                    part_R.append(p)
                part_R.append(depN)
                part_min = part_L
            #end for s
            
        #jesli zadna permutacja nie spelnia, to zwracamy -1
        if(part_R == []):
            return[-1, []]
        
        #znalezlismy najlepsza permutacje
        L += part_min
        R.append(part_R)

    #znalezlismy najlepsze rozwiazanie podproblemu
    return [L, R]
#dep_dist[vis][dep]
