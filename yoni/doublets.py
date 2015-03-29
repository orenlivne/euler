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

Created on Mar 28, 2015
@author: Oren Livne <oren.livne@gmail.com>
============================================================
'''
import networkx as nx

DIGITS = map(str, xrange(10))

def shortest_doublet_graph(lst):
    '''Returns the shortest path between the first and last element of lst in the undirected graph G whose
    nodes are the elements of the list lst of n m-digit numbers, and an edge between x and y exists if
    and only if y can be obtained from x (and vice versa, of course) by changing one digit.
    Runtime complexity: O(E + n log n) where E = number of edges of G.'''
    # Build the graph.
    if not lst: return []
    g = nx.Graph()
    s = set(map(str, lst))
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
    return map(int, nx.shortest_path(g, str(lst[0]), str(lst[-1])))

if __name__ == '__main__':
    print shortest_doublet_graph([123, 991, 323, 321, 329, 121, 921, 125, 999])
