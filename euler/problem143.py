'''
============================================================
http://projecteuler.net/problem=143

Let ABC be a triangle with all interior angles being less than 120 degrees. Let X be any point inside the triangle and let XA = p, XB = q, and XC = r.

Fermat challenged Torricelli to find the position of X such that p + q + r was minimised.

Torricelli was able to prove that if equilateral triangles AOB, BNC and AMC are constructed on each side of triangle ABC, the circumscribed circles of AOB, BNC, and AMC will intersect at a single point, T, inside the triangle. Moreover he proved that T, called the Torricelli/Fermat point, minimises p + q + r. Even more remarkable, it can be shown that when the sum is minimised, AN = BM = CO = p + q + r and that AN, BM and CO also intersect at T.

If the sum is minimised and a, b, c, p, q and r are all positive integers we shall call triangle ABC a Torricelli triangle. For example, a = 399, b = 455, c = 511 is an example of a Torricelli triangle, with p + q + r = 784.

Find the sum of all distinct values of p + q + r  120000 for Torricelli triangles.
============================================================
'''
from __future__ import division

area48 = lambda a, b, c: 3 * (a + b - c) * (a - b + c) * (-a + b + c) * (a + b + c)
f = lambda a, b, c: a ** 4 - 2 * (b ** 2 - c ** 2) ** 2 + a ** 2 * (b ** 2 + c ** 2 + area48(a, b, c) ** 0.5)

def distances(a, b, c):
    a1, a2, a3 = f(a, b, c), f(b, c, a), f(c, a, b)
    c2 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    c1 = (b ** 2 - c2 ** 2) ** 0.5
    # D = area48(a, b, c)
    # print '48*area^2 =', D, '=', D ** 0.5, '^ 2, y', D ** 0.5 / 3, D ** 0.5 / 27
    # print (a + b - c) , (a - b + c) , (-a + b + c) , (a + b + c)
    # print (a + b - c) % 3 , (a - b + c) % 3 , (-a + b + c) % 3, (a + b + c) % 3
    # print a % 3, b % 3, c % 3
    # print (a + b) % 3, (a - b) % 3
    # print 'c1', c1, c1 == int(c1), 'c2', c2, c2 == int(c2)
    # print a1, a1 == int(a1), a2, a2 == int(a2), a3, a3 == int(a3) 
    s = a1 + a2 + a3
    # print 's', s, s == int(s)
    T = (a3 * c1, a2 * c + a3 * c2)
    # print 'T', (T[0] / s, T[1] / s)
    pn = (T[0] ** 2 + T[1] ** 2) ** 0.5
    qn = (T[0] ** 2 + (T[1] - c * s) ** 2) ** 0.5
    rn = ((T[0] - c1 * s) ** 2 + (T[1] - c2 * s) ** 2) ** 0.5
    # print pn, pn == int(pn)
    # print pn, qn == int(qn)
    # print pn, rn == int(rn)
    p = pn / s
    q = qn / s
    r = rn / s
#    print p, q, r, p + q + r
    return p, q, r

#----------------------------------------------------------------------------------------------------
# Based on http://www.mathblog.dk/project-euler-143-investigating-the-torricelli-point-of-a-triangle/
#----------------------------------------------------------------------------------------------------
# His implementation
def sums2(pairs, limit):
    pairs = sorted(pairs)
    count = len(pairs)

    index = [-1] * limit
    for i, (u, _) in enumerate(pairs):
        if index[u] == -1: index[u] = i
 
    for i, (a, b) in enumerate(pairs):
        va, vb = list(), list()
        
        for j in xrange(index[a], count):
            p = pairs[j];
            if (p[0] != a): break
            va.append(p[1])

        for j in xrange(index[b], count):
            p = pairs[j];
            if (p[0] != b): break
            vb.append(p[1])

        for v in va:
            try:     
                if (vb.index(v) != -1 and a + b + v <= limit): yield (a, b, v)
            except ValueError: pass
            
# My implementation
from problem005 import gcd
import networkx as nx

def pairs(N):
    '''Generate the list S of pairs (x,y) s.t. x**2+y**2+x*y is a perfect square and x+y <= N.'''
    S = []
    for u in xrange(1, int(N ** 0.5) + 1):
        u2 = u * u
        for v in (v for v in xrange(1, u) if (u - v) % 3 != 0 and gcd(u, v) == 1):
            v2 = v * v
            p, r = 2 * u * v + v2, u2 - v2
            pr = p + r
            if pr > N: break
            #print 'u', u, 'v', v
            for k in xrange(1, int(N / float(pr)) + 1):
                #print '\t', 'k', k, (k * p, k * r)
                S.append((k * p, k * r))
    return S

def pairs2(N, add_both=True):
    pairs = list()
    for u in xrange(int(N ** 0.5) + 1):
        for v in xrange(1, u):
            if (gcd(u, v) != 1): continue;
            if ((u - v) % 3 == 0): continue;
            p = 2 * u * v + v * v
            r = u * u - v * v
            if p + r > N: break
            #print 'u', u, 'v', v
            for k in xrange(1, int(N / float(r + p)) + 1):
                #print '\t', 'k', k, (k * p, k * r)
                pairs.append((k * p, k * r))
                if add_both: pairs.append((k * r, k * p))
    return pairs

def triangles(G): 
    '''Yield all triangles in the undirected graph G.'''
    visited = set()
    for u in G: 
        visited.add(u)
        nbhr_visited, Gu = set(), set(G.neighbors(u))
        for v in (v for v in Gu if not v in visited):
            if not v in nbhr_visited:
                nbhr_visited.add(v)
                for w in (w for w in set(G.neighbors(v)) & Gu if not w in visited and not w in nbhr_visited): yield (u, v, w)

solution_set = lambda N: set(filter(lambda (p, q, r): p + q + r <= N, triangles(nx.from_edgelist(pairs(N)))))

if __name__ == "__main__":
    print sum(set([p + q + r for (p, q, r) in solution_set(120000)]))
