'''
============================================================
http://projecteuler.net/problem=107

The following undirected network consists of seven vertices and twelve edges with a total weight of 243.


The same network can be represented by the matrix below.

        A    B    C    D    E    F    G
A    -    16    12    21    -    -    -
B    16    -    -    17    20    -    -
C    12    -    -    28    -    31    -
D    21    17    28    -    18    19    23
E    -    20    -    18    -    -    11
F    -    -    31    19    -    -    27
G    -    -    -    23    11    27    -
However, it is possible to optimise the network by removing some edges and still ensure that all points on the network remain connected. The network which achieves the maximum saving is shown below. It has a weight of 93, representing a saving of 243  93 = 150 from the original network.

Using network.txt (right click and 'Save Link/Target As...'), a 6K text file containing a network with forty vertices, and given in matrix form, find the maximum saving which can be achieved by removing redundant edges whilst ensuring that the network remains connected.
============================================================
'''
from Queue import PriorityQueue

read_edges = lambda file_name: [(u, v, float(w)) for u, v, w in ((u, v, w) for u, line in enumerate(open(file_name, 'rb')) for v, w in enumerate(line.rstrip('\r\n').rstrip('\n').split(',')) if w != '-' and u < v)]

def max_savings(edge_list):
    n = max(e[1] for e in edge_list) + 1
    q, t, s, a = PriorityQueue(), range(n), [set([u]) for u in xrange(n)], 0
    for u, v, w in edge_list: q.put((w, (u, v)))
    while not q.empty():
        w, (u, v) = q.get()
        tu, tv = t[u], t[v]
        if tu != tv:
            sv = s[tv]
            for i in sv: t[i] = tu
            s[tu] |= sv
            sv.clear()
        else:
            a += w
    return a

if __name__ == "__main__":
    print max_savings(read_edges('problem107.dat'))
