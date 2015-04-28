import itertools as it, heapq

infinity = float("inf")

class Graph(object):
  def __init__(self, node_list, edge_list):
    self.nbhrs = dict()
    for node in node_list: self.add_node(node)
    for edge in edge_list: self.add_edge(edge[0], edge[1], edge[2])

  def add_node(self, u):
    self.nbhrs.setdefault(u, {})
    
  def add_edge(self, u, v, weight):
    self.nbhrs.setdefault(u, {}).__setitem__(v, weight)
    self.nbhrs.setdefault(v, {}).__setitem__(u, weight)

  def number_of_edges(self):
    return sum(len(nbhrs) for nbhrs in self.nbhrs.itervalues())/2

  def __iter__(self):
    return self.nbhrs.__iter__()

  def __str__(self):
    return 'Graph[' + ','.join(map(str, ((u,v) for u in self.nbhrs for v in self.nbhrs[u]))) + ']'

class PriorityQueue(object):
  REMOVED = -100000      # placeholder for a removed task.

  def __init__(self, tasks_and_priorities=[]):
    self.pq = []                         # list of entries arranged in a heap
    self.entry_finder = {}               # mapping of tasks to entries
    self.counter = it.count()            # unique sequence count
    for task, priority in tasks_and_priorities: self.add(task, priority)

  def add(self, task, priority):
    # Add a new task or update the priority of an existing task.
    if task in self.entry_finder: self.remove(task)
    self.count = next(self.counter)
    entry = [priority, self.count, task]
    self.entry_finder[task] = entry
    heapq.heappush(self.pq, entry)

  def remove(self, task):
    # Mark an existing task as REMOVED.  Raise KeyError if not found.
    entry = self.entry_finder.pop(task)
    entry[-1] = PriorityQueue.REMOVED

  def __len__(self):
    return sum(1 for _, _, task in self.pq if task != PriorityQueue.REMOVED)

  def pop(self):
    # Remove and return the lowest priority task. Raise KeyError if empty.
    while self.pq:
      priority, count, task = heapq.heappop(self.pq)
      if task != PriorityQueue.REMOVED:
        del self.entry_finder[task]
        return task, priority
    raise KeyError('pop from an empty priority queue')

def shortest_path_distance(g, source):
  # Returns the shortest path distance from source to any node in g and
  # a dictionary prev with a pointers to the "next-hop" node on the source graph
  # to get the shortest route to the source.

  # Initialize distances and previous nodes. All nodes initially in Q (unvisited nodes).
  dist = dict((v, 0 if v == source else infinity) for v in g)
  prev = dict((v, None) for v in g)
  Q = PriorityQueue((v, dist[v]) for v in g) # Unvisited nodes.

  while Q:
    # Unvisited node with minimum distance from source. Initially, the source node.
    u, dist_u = Q.pop()
    for v, weight in g.nbhrs[u].iteritems():  # where v is still in Q.
      alt = dist_u + weight
      if alt < dist[v]:               # A shorter path to v has been found.
        dist[v] = alt
        Q.add(v, alt)
        prev[v] = u
  return dist, prev

def can_pass(a, first, second):
  m, n = len(a), len(a[0])
  g = Graph(((i, j) for i in xrange(m) for j in xrange(n)),
            (((u, v, 1) for u, v in
              it.ifilter(lambda ((i, j), (k, l)): a[i][j] == a[k][l],
                         it.chain(
                             (((i, j), (i - 1, j)) for i in xrange(1, m) for j in xrange(n)),
                             (((i, j), (i + 1, j)) for i in xrange(m - 1) for j in xrange(n)),
                             (((i, j), (i, j - 1)) for i in xrange(m) for j in xrange(1, n)),
                             (((i, j), (i, j + 1)) for i in xrange(m) for j in xrange(n - 1))
                             )
                       )
            )))
  dist, _ = shortest_path_distance(g, first)
  return dist[second] != infinity


if __name__ == '__main__':
  assert can_pass(((1,9),(9,1)), (0,1), (1,0)) == False, '2x2 checkerboard'
  assert can_pass(((0, 0, 0, 0, 0, 0),
                   (0, 2, 2, 2, 3, 2),
                   (0, 2, 0, 0, 0, 2),
                   (0, 2, 0, 2, 0, 2),
                   (0, 2, 2, 2, 0, 2),
                   (0, 0, 0, 0, 0, 2),
                   (2, 2, 2, 2, 2, 2),),
                  (3, 2), (0, 5)) == True, 'First example'
assert can_pass(((0, 0, 0, 0, 0, 0),
                 (0, 2, 2, 2, 3, 2),
                 (0, 2, 0, 0, 0, 2),
                 (0, 2, 0, 2, 0, 2),
                 (0, 2, 2, 2, 0, 2),
                 (0, 0, 0, 0, 0, 2),
                 (2, 2, 2, 2, 2, 2),),
                (3, 3), (6, 0)) == False, 'First example'
