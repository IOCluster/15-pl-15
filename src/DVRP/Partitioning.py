def algorithm_u(ns, m):
    """Algorytm znajdujacy wszystkie podzialy o licznosci m zbioru ns ( tzn. m zbiorow w podziale)""" 
    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)
        
def pretty_print(parts):
    print( '; '.join('|'.join(''.join(str(e) for e in loe) for loe in part) for part in parts))


def Partition(n_nodes, n_depots, n_visits, which_node):
    P = [i+n_depots for i in range(n_visits)]
    l = len(P)
    count = 0;
    for k in range(1, l):
        if(k == 1):
            yield [P]
        else:
            parts = algorithm_u(P, k)
            count  = 0;
            for part in parts:
                count = (count + 1) % n_nodes
                if(count == which_node):
                    part = yield part          


def PartitionProblem(vrp, n_nodes, which_node):
    P = [i+vrp.num_depots for i in range(vrp.num_visits)]
    l = len(P)
    count = 0
    for k in range(1, l):
        if(k == 1):
            if(sum(vrp.demands[i-vrp.num_depots] for i in P) < vrp.caps):
                yield [P]
        else:
            parts = algorithm_u(P, k)
            count  = 0
            for part in parts:
                count = (count + 1) % n_nodes
                if(count == which_node):
                    check = True
                    for loe in part:
                        check &= (sum(vrp.demands[i-vrp.num_depots] for i in loe) < vrp.caps)
                    if(check):
                        part = yield part   
               

