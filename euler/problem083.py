'''
============================================================
http://projecteuler.net/problem=83

OTE: This problem is a significantly more challenging version of Problem 81.

In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by moving left, right, up, and down, is indicated in bold red and is equal to 2297.

131    673    234    103    18
201    96    342    965    150
630    803    746    422    111
537    699    497    121    956
805    732    524    37    331

Find the minimal path sum, in matrix.txt (right click and 'Save Link/Target As...'), a 31K text file containing a 80 by 80 matrix, from the top left to the bottom right by moving left, right, up, and down.
============================================================
'''
import numpy as np, itertools as it, heapq

'''Translate a 0-based index into a 1-based index.'''
inc = lambda x: (x[0] + 1, x[1] + 1)

nbhrs = lambda (i, j): [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

def shortest_path_len_matrix(A, source, target):
    '''Return the length of the shortest path between source and target in the cost matrix A using
    Dijkstra''s algorithm.
    @see http://en.wikipedia.org/wiki/Dijkstra''s_algorithm'''
    # Pad A with a layer of dummy visited nodes and use 1-based indexing in the original entries for
    # easier neighbor finding 
    inf, A, source, target, (m, n) = np.iinfo(np.uint).max, np.lib.pad(A, (1, 1), 'constant'), inc(source), inc(target), A.shape
    visited, dist = np.zeros_like(A, dtype=np.bool), np.zeros_like(A, dtype=np.uint)
    visited[np.array([0, m + 1]), :] = True
    visited[:, np.array([0, n + 1])] = True
    dist.fill(inf)
    dist[source] = A[source]
    Q = MyHeapq([(u, dist[u]) for u in it.product(xrange(1, m + 1), xrange(1, n + 1))])
    while Q:
        u, d = Q.pop_task()
        #print u, d
        if u == target: return d
        visited[u] = True
        for v in (v for v in nbhrs(u) if not visited[v]):
            alt = d + A[v]
            if alt < dist[v]:
                dist[v] = alt
                Q.add_task(v, alt)
    raise ValueError('No path from %s to %s' % (repr(source), repr(target)))

class MyHeapq(object):
    def __init__(self, tasks):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = it.count()  # unique sequence count
        for task, priority in tasks: self.add_task(task, priority)
    
    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)
    
    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
    
    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, _, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task, priority
        raise KeyError('pop from an empty priority queue')

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    A = np.loadtxt('problem081.dat', delimiter=',', dtype=np.uint) 
    print shortest_path_len_matrix(A, (0, 0), (A.shape[0] - 1, A.shape[1] - 1))
    A = np.loadtxt('problem082-sample.dat', delimiter=',', dtype=np.uint) 
    print shortest_path_len_matrix(A, (0, 0), (A.shape[0] - 1, A.shape[1] - 1))
