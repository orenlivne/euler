'''
============================================================
http://projecteuler.net/problem=68

Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.

Working clockwise, and starting from the group of three with the numerically lowest external node (4,3,2 in this example), each solution can be described uniquely. For example, the above solution can be described by the set: 4,3,2; 6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12. There are eight solutions in total.

Total    Solution Set
9    4,2,3; 5,3,1; 6,1,2
9    4,3,2; 6,2,1; 5,1,3
10    2,3,5; 4,5,1; 6,1,3
10    2,5,3; 6,3,1; 4,1,5
11    1,4,6; 3,6,2; 5,2,4
11    1,6,4; 5,4,2; 3,2,6
12    1,5,6; 2,6,4; 3,4,5
12    1,6,5; 3,5,4; 2,4,6
By concatenating each group it is possible to form 9-digit strings; the maximum string for a 3-gon ring is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit strings. What is the maximum 16-digit string for a "magic" 5-gon ring?
============================================================
'''
import numpy as np, itertools as it, sys

class RingPosition(object):
    def __init__(self, v, free_nodes, free):
        '''Initialize a ring position from a numpy values array at nodes and a set of free values that
        have not yet been placed.'''
        self.v = v
        self.free_nodes = free_nodes
        self.free = free
    
    @staticmethod
    def nbhrs(i):
        return [(i - 1, (i + 1) % 10)] if i % 2 == 1 else [(i + 1, (i + 2) % 10), ((i - 1) % 10, (i - 2) % 10)]

    def is_legal(self, s):
        v = self.v
        for i in xrange(1, 10, 2):
            N = np.array(RingPosition.nbhrs(i)[0])
            if sum(v[N]) != s - v[i]:
                return False
        return True

    def __repr__(self):
        return 'Ring[v=' + repr(self.v) + ', free_nodes=' + repr(self.free_nodes) + ', free=' + repr(self.free) + ']'
        
    @property
    def lexstr(self):
        v = self.v
        i = 2 * np.argmin(v[1::2]) + 1
        return ''.join(str(v[(i + 2 * j) % 10]) + ''.join(map(str, v[np.array(RingPosition.nbhrs((i + 2 * j) % 10)[0])]))
                      for j in xrange(5))
    
    def move(self, i, w):
        v = self.v.copy()
        v[i] = w
        return RingPosition(v, self.free_nodes - set([i]), self.free - set([w]))
    
    def legal_moves(self, s):
        for i in self.free_nodes:
            nbhrs = RingPosition.nbhrs(i)
            print '\ti', i, 'nbhrs', nbhrs
            for x in reduce(set.__and__, (set(self.legal_moves_on_line(s, i, N)) for N in RingPosition.nbhrs(i))):
                yield x
            
    def legal_moves_on_line(self, s, i, N):
        '''Return a list of all legal moves at i along the line where i''s neighbors are the list N.'''
        sys.stdout.write('\tlegal_moves_on_line(%d, %s) ' % (i, repr(N)))
        v0, v1, F = self.v[N[0]], self.v[N[1]], self.free
        if v0 and v1:  # closed move
            w = s - v0 - v1
            print [(i, w)] if w in F else []
            return [(i, w)] if w in F else []
        elif v0 or v1:  # semi-open move
            s2 = s - (v0 if v0 else v1)
            print [(i, w) for w in F if s2 - w in F]
            return [(i, w) for w in F if s2 - w in F]
        else:  # open move
            print [(i, w) for w in F]
            return [(i, w) for w in F]

def dfs(pos, s):
    '''Depth-first search that outputs all legal ring solutions, starting from the initial
    position pos and with line sum s.'''
    print 'dfs pos', pos
    if not pos.free:
        print 'Found solution', pos
        yield pos.lexstr
    moves = list(pos.legal_moves(s))
    print 'moves', moves
    for (i, w) in moves:
        for x in dfs(pos.move(i, w), s):
            yield x
                
     
def solve_ring(s):
    initial = RingPosition(np.zeros((10,), dtype=np.byte), set(range(10)), set(range(1, 11)))
    # print list(dfs(initial.move(0, 10), s))
    # print list(dfs(initial.move(1, 10), s))
    return max(max(map(str, dfs(initial.move(0, 10), s))),
               max(map(str, dfs(initial.move(1, 10), s))))
    
def solve_ring_brute_force(s):
#     return [r.lexstr for r in (RingPosition(np.array((10,) + x), [], []) 
#                                for x in it.permutations(range(1, 10), 9)) if r.is_legal(s)] + \
    return [r.lexstr for r in (RingPosition(np.array((x[0], 10) + x[1:]), [], []) 
                               for x in it.permutations(range(1, 10), 9)) if r.is_legal(s)]

#----------- recursive's solition 26 Jan 2007 -----------
constraint = [lambda c: True] * 10
constraint[0] = lambda c: c[0] == 10
constraint[4] = lambda c: c[0] + c[1] == c[3] + c[4]
constraint[6] = lambda c: c[2] + c[3] == c[5] + c[6]
constraint[8] = lambda c: c[4] + c[5] == c[7] + c[8]
constraint[9] = lambda c: c[6] + c[7] == c[1] + c[9]

def solve_ring_recursive():
    sides, rots = [0, 1, 2, 3, 2, 4, 5, 4, 6, 7, 6, 8, 9, 8, 1], []
    for i in xrange(0, len(sides), 3): rots.append(sides[i:] + sides[:i])
    #print rots
    
    search, sols = [[]], []
    while search:
        c = search.pop()
        print c
        left = set(range(1, 11)) - set(c)
        if len(left) == 0:
            sols.append(c)
            #print 'sol', c
        for cv in left:
            if constraint[len(c)](c + [cv]): search.append(c + [cv])
    #print sols
    for sol in sols:
        sol[:] = min([sol[cidx] for cidx in rot] for rot in rots)
    
    print ''.join(map(str, max(sols)))

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    solve_ring_recursive() #6531031914842725
    
#     r = RingPosition(np.array([5, 10, 1, 8, 7, 6, 3, 4, 9, 2]), [], [])
#     print r, r.is_legal(16), r.lexstr, len(r.lexstr)
#     for s in xrange(13, 21):
#         print s, solve_ring_brute_force(s)
    # print solve_ring(16)
