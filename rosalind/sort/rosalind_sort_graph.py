'''
============================================================
http://rosalind.info/problems/sort

A reversal of a permutation can be encoded by the two indices at the endpoints of the interval that it inverts; for example, the reversal that transforms (4,1,2,6,3,5) into (4,1,3,6,2,5) is encoded by [3,5].

A collection of reversals sorts p into g if the collection contains drev(p,g) reversals, which when successively applied to p yield g.

Given: Two permutations p and g, each of length 10.

Return: The reversal distance drev(p,g), followed by a collection of reversals sorting p into g. If multiple collections of such reversals exist, you may return any one.

============================================================
'''
from collections import deque
import os, networkx as nx
from rosalind.rear import rosalind_rear as rr


# Trying to generate the entire permutation graph. But it's too big - infeasible

def all_reverses_and_weights(p):
    '''A generator of all possible reverses of a permutation p.'''
    n = len(p)
    return ((rr.reverse(p, (j, k)), (j, k)) for j in xrange(n - 1) for k in xrange(j + 2, n + 1))

def _reversal_edgelist(n):
    '''Generator the edge list of the reversal graph of all permutations of length n.'''
    # Permutations are encoded as tuples.
    i = tuple(xrange(n))  # Identity permutation
    # Breadth-first search (BFS) 
    q, count, d = deque([i]), 0, {i: 0}  # d = Reversal distance dictionary. d[p] = d(p,i)
    while q:
        count += 1
        if count % 100000 == 0: print count, 'queue size', len(q) 
        x = q.popleft()
        dy = d[x] + 1
        for y, w in all_reverses_and_weights(x):
            if x < y:
                yield x, y, w
                # yield perm_hash(x, n), perm_hash(y, n), w
            if not y in d:
                d[y] = dy
                q.append(y)

def perm_hash(s, n):
    '''Return an array with a (rolling) hash of s[:j], j=0..len(s).'''
    h = 0L
    for x in s: h = n * h + x
    return h

def reversal_graph(n):
    g = nx.Graph()
    g.add_weighted_edges_from(_reversal_edgelist(n))
    return g

def read_graph(n, file_name):
    with open(file_name, 'rb') as f:
        g = nx.Graph()
        g.add_weighted_edges_from((tuple(map(int, x[0:n])), tuple(map(int, x[n:2 * n])), (int(x[2 * n]), int(x[2 * n + 1]))) for x in (x.split() for x in f))
        # g.add_weighted_edges_from((long(x[0]), long(x[1]), (int(x[2]), int(x[3]))) for x in (x.split() for x in f))
        return g
    
def write_graph(n, g, file_name):
    with open(file_name, 'wb') as f:
        for u, u_nbhrs in g.adjacency_iter():
            for v, e_attr in u_nbhrs.items():
                j, k = e_attr['weight']
                f.write('%s %s %d %d\n' % (' '.join(map(str, u)), ' '.join(map(str, v)), j, k))            

def write_edgelist(n, file_name):
    with open(file_name, 'wb') as f:
        for x in _reversal_edgelist(n):
            f.write('%d %d %d %d\n' % (x[0], x[1], x[2][0], x[2][1]))

def read_or_create_reversal_graph(n):
    file_name = 'reversal_graph_%d.txt' % (n,)
    if os.path.exists(file_name): return read_graph(n, file_name)
    else:
        g = reversal_graph(n)
        write_graph(n, g, file_name)
        # write_edgelist(n, file_name)
        #return read_graph(n, file_name)
        return g

def pinv(a):
    '''Inverse permutation of a.'''
    n = len(a)
    b = [0] * n
    for i in xrange(n): b[a[i]] = i
    return tuple(b)

def pmult(a, b):
    '''Multiply (compose) permutations: a o b.'''
    n = len(a)
    c = [0] * n
    for i in xrange(n): c[i] = a[b[i]]
    return tuple(c)

def rev_dist(s, t, d):
    '''Return the reversal distance of permutations s, t. Fetch from the hash d.'''
    return d[pmult(pinv(t), s)]

def reversal_sort_log(g, s, t):
    n = len(s)
    # print perm_hash(s, n), perm_hash(t, n)
    path = nx.shortest_path(g, perm_hash(s, n), perm_hash(t, n))
    print len(path) - 1
    for i in xrange(len(path) - 1):
        j, k = g[path[i]][path[i + 1]]['weight']
        print j + 1, k

def ros_sort(file_name, debug=0, g=None):
    '''Solution to the question. Prepares a hash d if doesn\'t exist yet, then fetches the entries
    of t^{-1}*s from d to find reversal_distance(t,s).'''
    with open(file_name, 'rb') as f: s, t = rr.to_int_list(f.next()), rr.to_int_list(f.next())
    if not g: g = read_or_create_reversal_graph(len(s))
    reversal_sort_log(g, s, t)
            
if __name__ == "__main__":
    g = read_or_create_reversal_graph(5)
    print g.nodes()
    print nx.shortest_path(g, (3, 0, 4, 2, 1), (0, 1, 2, 3, 4))
    print nx.shortest_path(g, (4, 1, 3, 0, 2), (1, 2, 0, 4, 3))
    # reversal_sort_log(g, (4, 1, 3, 0, 2), (1, 2, 0, 4, 3))
    # ros_sort('rosalind_sort_sample1.dat', g=g)
    
    # ros_sort('rosalind_sort_sample.dat', debug=1)
    # ros_sort('rosalind_sort.dat', debug=1)
