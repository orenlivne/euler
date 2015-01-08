'''
============================================================
http://projecteuler.net/problem=213

A 30x30 grid of squares contains 900 fleas, initially one flea per square.
When a bell is rung, each flea jumps to an adjacent square at random (usually 4 possibilities, except for fleas on the edge of the grid or at the corners).

What is the expected number of unoccupied squares after 50 rings of the bell? Give your answer rounded to six decimal places.
============================================================
'''
import numpy as np, itertools as it

# General dimension solution - slower
def time_step_nd(p):
    '''Advance a flee''s cell occupancy PDF from t-1 to t.'''
    q, offset = np.zeros_like(p), np.array([y for x in np.eye(p.ndim, dtype=int) for y in (x, -x)])
    for i_raw in it.product(*map(xrange, p.shape)):
        i = np.array(i_raw)
        nbhrs = np.array(filter(lambda x: all(x >= 0) and all(x < p.shape), i + offset))
        delta = p[map(np.array, i_raw)] / len(nbhrs)
        q[[nbhrs[:, j] for j in xrange(p.ndim)]] += delta
    return q
 
def flee_occupancy_nd(sz, i, t):
    '''Return the cell occupancy of a flee that starts at (i,j) after t time steps.'''
    p = np.zeros(sz); p[map(np.array, i)] = 1.0
    for _ in xrange(t): p = time_step_nd(p)
    return p
 
'''Expected number of non-occupied squares in a 2-D grid of size sz after t time steps.'''
no_occupancy_nd = lambda  sz, t: np.sum(reduce(lambda a, b: a * b, ((1 - flee_occupancy_nd(sz, i, t)) for i in it.product(*map(xrange, sz))), np.ones(sz)))

# 2-D solution - faster
def time_step(p):
    '''Advance a flee''s cell occupancy PDF from t-1 to t.'''
    q, (m, n) = np.zeros_like(p), p.shape
    in_grid = lambda (k, l): k >= 0 and k < m and l >= 0 and l < n
    for i, j in it.product(xrange(m), xrange(n)):
        nbhrs = filter(in_grid, ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)))
        delta = p[i, j] / len(nbhrs)
        for k, l in nbhrs: q[k, l] += delta
    return q

def flee_occupancy(sz, (i, j), t):
    '''Return the cell occupancy of a flee that starts at (i,j) after t time steps.'''
    p = np.zeros(sz); p[i, j] = 1.0
    for _ in xrange(t): p = time_step(p)
    return p

'''Expected number of non-occupied squares in a 2-D grid of size sz after t time steps.'''
no_occupancy = lambda  sz, t: np.sum(reduce(lambda a, b: a * b,
                                         ((1 - flee_occupancy(sz, i, t)) 
                                          for i in it.product(*(xrange(s) for s in sz))),
                                         np.ones(sz)))

if __name__ == "__main__":
    # print flee_occupancy((3, 3), (1, 1), 4)
    # for t in xrange(50): print t, no_occupancy((4, 4), t)
    # Approximated pretty well by by num_cells / e
    print '%.6f' % (no_occupancy((20, 10), 20),)
    print '%.6f' % (no_occupancy_nd((5, 5, 5), 10),)
    print '%.6f' % (no_occupancy((30, 30), 50),)
