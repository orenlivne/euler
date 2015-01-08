'''
============================================================
http://projecteuler.net/problem=

============================================================
'''
import numpy as np, itertools as it

def d_solution(a, b, c, d1):
    d = np.zeros((4,), dtype=float)
    A = a[0] + a[3]
    e = c[0] + c[1] - (b[0] + b[2])
    f = b[1] + b[2] + c[1] + c[2] - A
    # d[0 ]= (c[2 ]+ c[3] - (c[0] + c[1]) + e + f) / 2.
    d[0] = (c[1] + 2 * c[2] + c[3] - b[0] + b[1] - A) / 2.
    d[3 ] = f - d[0]
    # d[3] = (b[0] + b[1] + 2 * b[2] + c[1] - c[3] - A) / 2.
    d[1] = d1
    d[2] = d1 + e
    return d

def residual(a, b, c, d):
    return np.array([
                     d[0] + d[1] + c[0] + c[1] - (d[2] + d[3] + c[2] + c[3]),
                     d[0] + d[2] + b[0] + b[2] - (d[1] + d[3] + b[1] + b[3]),
                     d[0] + d[1] + c[0] + c[1] - (d[0] + d[2] + b[0] + b[2]),
                     d[0] + d[3] + a[0] + a[3] - (b[1] + b[2] + c[1] + c[2])]
                     )

def sums(a, b, c, d):
    A = np.array([[a[0], a[1], b[0], b[1]], [a[2], a[3], b[2], b[3]],
                  [c[0], c[1], d[0], d[1]], [c[2], c[3], d[2], d[3]]])
    print ''
    print A
    return np.array([sum(A[i, :]) for i in xrange(4)] + 
                    [sum(A[:, i]) for i in xrange(4)] + 
                    [sum(A[i, i] for i in xrange(4)), sum(A[i, 3 - i] for i in xrange(4))])

def num_magic():
    s = 0
    # for a0, a1, a2, a3 in [(0, 0, 0, 0)]:
    for a0, a1, a2, a3 in it.product(*(xrange(10) for _ in xrange(4))):  # a is free
        a = (a0, a1, a2, a3) 
        print 'a', a
        A, i = a0 + a3, a0 + a1 - (a2 + a3)
        na = 3 * a0 + 2 * a1 + a3
        # Find all permissible b's
        for b0, b1 in it.product(*(xrange(10) for _ in xrange(2))):
            j, l = i + b0 + b1, (A + b0 - b1) % 2
            for b2 in xrange(max(0, j - 9), min(j, 9) + 1):  # B(I)
                b3, h = j - b2, b0 + b1 + 2 * b2 - A  # B(II)
                B = b0 + b1 + b2 + b3
                nb = b0 - b1 - 2 * b2 - 2 * b3
                q = a0 + a1 - b0 - b2
                r = B - q
                print '\t', 'b', (b0, b1, b2, b3)
                # Find all permissible c's
                for c3 in xrange(max(0, r - 9), min(r, 9) + 1):  # B(I)
                # for c3 in xrange(10):
                    p = na + nb + c3
                    t = 2 * (q - b1 - b3) + p
                    for c1 in (c1 for c1 in xrange(max(0, c3 - h, p - 18, q - 9, t - 9), min(9, 18 + c3 - h, p, q, t) + 1) if (c1 + c3) % 2 == l):  # C(I),C(II)
                        # k = B - (c1 + c3)
                        # for c2 in xrange(max(0, k - 9), min(k, 9) + 1):  # C(III))
                        c2 = q - c1
                        s += 1

                        c0 = B - (c1 + c2 + c3)
                        print '\t\t', 'c', (c0, c1, c2, c3)  # , 'solutions', 10 + min(e, 0) - max(e, 0)
                        bb = (b0, b1, b2, b3)
                        cc = (c0, c1, c2, c3)
                        d0 = (c1 + 2 * c2 + c3 - b0 + b1 - A) / 2.
                        d1 = (na + 3 * b0 + b1 - 2 * c0 - 3 * c1 - 2 * c2 - c3) / 2.
                        d1_v2 = (p - c1) / 2.
                        print '\t\t', 'd0', d0, 'd1', d1, d1_v2, 'res', a0 + a1 + b0 + b1 - (c0 + c1 + d0 + d1)
                        d = d_solution(a, bb, cc, d1_v2)
                        ss = sums(a, bb, cc, d)
                        print '\t\t\t', 'd', d, ss, residual(a, bb, cc, d)
                        if any(np.diff(ss) != 0):
                            raise ValueError('Wrong solution')
    return s

# Trying to parameterize using the first column, with a lookup table of 
def num_magic2():
    b = [[[x for x in it.product(*(xrange(10) for _ in xrange(3))) if sum(x) == s - a] for a in xrange(10)] for s in xrange(37)]  # @UndefinedVariable @UnusedVariable
    tot = 0
    for a0, b0, c0, d0 in it.product(*(xrange(10) for _ in xrange(4))):
        s = a0 + b0 + c0 + d0
        sol = sum(1 for (x, y, z, w) in #@UnusedVariable
                  ((x, y, z, (s - (x[0] + y[0] + z[0]),
                              s - (x[1] + y[1] + z[1]),
                              s - (x[2] + y[2] + z[2]))) 
                   for x, y, z in it.product(b[s][a0], b[s][b0], b[s][c0])) 
                  if min(w) >= 0 and max(w) <= 9 
                  and a0 + y[0] + z[1] + w[2] == s
                  and x[2] + y[1] + z[0] + d0 == s)
        tot += sol
        print (a0, b0, c0, d0), sol, tot
    return tot
    
if __name__ == "__main__":
    print num_magic2()
