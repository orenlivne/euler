class Graph(object):
  def __init__(self, edge_list):
    self.nbhrs = dict()
    for edge in edge_list: self.add_edge(edge[0], edge[1])

    def add_edge(self, u, v):
      self.nbhrs.setdefault(u, set([])).add(v)
      self.nbhrs.setdefault(v, set([])).add(u)

    def __repr__(self):
      print 'Graph edges:'
      for u in self.nbhrs:
        for v in self.nbhrs[u]:
          print u, v

if __name__ == '__main__':
#      t = [('121', '123'), ('123', '193'), ('193', '993'), ('121', '125')
#      g = Graph([('121', '123'), ('123', '193'), ('193', '993'), ('121', '125')]
      g = Graph([('x', 'y'), ('y', 'z'), ('y', 'steve'), ('steve', 'oren')])
      print g
