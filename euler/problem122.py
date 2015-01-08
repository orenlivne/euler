'''
============================================================
http://projecteuler.net/problem=122

The most naive way of computing n15 requires fourteen multiplications:

n  n  ...  n = n15

But using a "binary" method you can compute it in six multiplications:

n  n = n2
n2  n2 = n4
n4  n4 = n8
n8  n4 = n12
n12  n2 = n14
n14  n = n15

However it is yet possible to compute it in only five multiplications:

n  n = n2
n2  n = n3
n3  n3 = n6
n6  n6 = n12
n12  n3 = n15

We shall define m(k) to be the minimum number of multiplications to compute nk; for example m(15) = 5.

For 1  k  200, find  m(k).
============================================================
'''
import numpy as np

def mk(n):
    P, l = [[] for _ in xrange(n + 1)], np.zeros((n + 1,), dtype=np.int)
    P_bf = [[] for _ in xrange(n + 1)]
    P[1].append(frozenset([]))
    P_bf[1].append(frozenset([]))
    for k in xrange(2, n + 1):
#         print 'k', k
#         l_max = np.array([max(l[m], l[k - m]) for m in xrange(1, int(k / 2) + 1)], dtype=np.int)
#         l_max_min = min(l_max)
#         m_star = np.where(l_max == l_max_min)[0] + 1
#         print '\t', l[1:k]
#         print '\t', 'l_max_min', l_max_min, l_max
#         print '\t', 'm_star', m_star
#         Q = np.unique([p | q for m in m_star for p in P[m] for q in P[k - m]])
#         lq = np.array(map(len, Q))
#         l_min = min(lq)
        K = frozenset([k])
#         P[k] = [p | K for p in Q[np.where(lq == l_min)[0]]]
#         l[k] = l_min + 1

        Q_bf = np.unique([p | q for m in xrange(1, int(k / 2) + 1) for p in P_bf[m] for q in P_bf[k - m]])
        lq = np.array(map(len, Q_bf))
        l_min = min(lq)
        P_bf[k] = [p | K for p in Q_bf[np.where(lq == l_min)[0]]]
        # l_bf = l_min + 1
        l[k] = l_min + 1
#         if set(P[k]) != set(P_bf[k]):
#             print '\t', '--->', l[k], l_bf
#             print '\t', 'P_bf', P_bf[k]
#             print '\t', 'P', P[k]
#             return None 
        print k, l[k], len(P_bf[k])#, P_bf[k]
#    print l_bf
    print l
#   print np.where(l != l_bf)[0]
    return l

if __name__ == "__main__":
    print sum(mk(200))
