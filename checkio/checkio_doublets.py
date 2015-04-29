'''
============================================================
Doublets, sometimes known as Word ladder, is a word game
invented by Charles Dodgson (aka Lewis Carroll). A doublets
puzzle begins with two words. To solve the puzzle one must
find a chain of different words to link the two together
such that the two adjacent words differ by one letter.
For Example:
FLOUR => FLOOR => FLOOD => BLOOD => BROOD => BROAD => BREAD
The Robots like using digits more than letters, so we've
changed the rules a little. You are given the list of numbers
with exactly the same length and you must find the shortest
chain of numbers to link the first number to the last like
you would with the words. For Example. There is a list
[123, 991, 323, 321, 329, 121, 921, 125, 999]. The shortest
way from the first to the last is: 123 => 121 => 921 => 991 => 999
You should write a function that receives a list of numbers
(positive integers) and returns the shortest route as a list
of numbers.
Input: Numbers as a list of integers.
Output: The shortest chain from the first to the last number
as a list of integers.

http://www.checkio.org/mission/digits-doublets/

Created on Mar 28, 2015
@author: Oren Livne <oren.livne@gmail.com>
============================================================
'''
import networkx as nx

DIGITS = map(str, xrange(10))

def shortest_path_graph(lst):
    '''Returns the shortest path between the first and last element of lst in the undirected graph G whose
    nodes are the elements of the list lst of n m-digit number strings, and an edge between x and y exists if
    and only if y can be obtained from x (and vice versa, of course) by changing one digit.
    Runtime complexity: O(E + n log n) where E = number of edges of G.'''
    if not lst: return []

    # Build the graph.
    g = nx.Graph()
    s = set(lst)
    m = len(s.__iter__().next())
    for x in s:
        # For each x, find all the possible graph neighbors that are one-digit away. Add edges to g
        # for those that are present in s.
        for i in xrange(m):
            tweaked_digits = list(x)
            for different_digit in (d for d in DIGITS if d != x[i]):
                tweaked_digits[i] = different_digit
                y = ''.join(tweaked_digits)
                if y in s: g.add_edge(x, y)
                
    # Use Dijkstra's algorithm to find the shortest path between the first and last elements of lst.
    return nx.shortest_path(g, str(lst[0]), str(lst[-1]))

def one_digit_apart(x, y):
    return sum(xi != yi for xi, yi, in zip(x, y)) == 1  
 
def shortest_path_steve(numbers):
    if not numbers: return []
    first, last = numbers[0], numbers[-1]
    paths = [[last]]
    
    # Breadth-first search in the one-digit-apart graph: keep a list of paths ending
    # with last. Augment each one with the neighbors of the first node on the path
    # until we find one that starts with last.
    num_paths = 0 
    for path in paths:
        num_paths += 1
        if num_paths % 100000 == 0: print num_paths, path
        for i in numbers[:-1]:
            # The shortest path cannot have cycles, so only check paths of distinct nodes,
            # hence the first check.
            if i not in path and one_digit_apart(i, path[0]):
                augmented_path = [i] + path
                if i == first: return augmented_path
                else: paths.append(augmented_path)

# A solution without networkx.
class MyGraph(object):
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
    numbers = map(str, [123, 991, 323, 321, 329, 121, 921, 125, 999])
    print shortest_path_graph(numbers)
    print shortest_path_steve(['991', '999'])
    
    ladder = sorted([('%d%d%d' % (i, i, i)) for i in xrange(10)] + \
    [('%d%d%d' % (i, i, i + 1)) for i in xrange(9)] + \
    [('%d%d%d' % (i, i, i - 1)) for i in xrange(1, 10)] + \
    [('%d%d%d' % (i, i+1, i)) for i in xrange(9)] + \
    [('%d%d%d' % (i, i-1, i)) for i in xrange(1, 10)] + \
    [('%d%d%d' % (i+1, i, i)) for i in xrange(9)] + \
    [('%d%d%d' % (i-1, i, i)) for i in xrange(1, 10)])
    print ladder
    print shortest_path_graph(ladder)
    print shortest_path_steve(ladder)
