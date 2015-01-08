'''
============================================================
http://projecteuler.net/problem=433

Let E(x0, y0) be the number of steps it takes to determine the greatest
common divisor of x0 and y0 with Euclid's algorithm. More formally:
x1 = y0, y1 = x0 mod y0
xn = yn-1, yn = xn-1 mod yn-1
E(x0, y0) is the smallest n such that yn = 0.

We have E(1,1) = 1, E(10,6) = 3 and E(6,10) = 4.

Define S(N) as the sum of E(x,y) for 1  x,y  N.
We have S(1) = 1, S(10) = 221 and S(100) = 39826.

Find S(5 x 10^6).
============================================================
'''
#from euler.problem127 import rad
from euler.problem070 import phi
from euler.problem005 import gcd

def gcd_steps(x, y):
    count = 0
    while y: x, y, count = y, x % y, count + 1
    return count

def gcd_and_steps(x, y):
    count = 0
    while y: x, y, count = y, x % y, count + 1
    return x, count

S = lambda N: sum(gcd_steps(x, y) for x in xrange(1, N + 1) for y in xrange(1, N + 1))
T = lambda n: sum(gcd_steps(n, m) for m in xrange(n))

tau_restricted = lambda n, r: sum(k for d, k in (gcd_and_steps(m, n) for m in xrange(r)) if d == 1)  # @UnusedVariable
tau = lambda n: tau_restricted(n, n)


if __name__ == "__main__":
    N = 100
    print S(N), 2 * sum(T(n) for n in xrange(1, N + 1)) + N * (N + 1) / 2

    print gcd_steps(47, 13)
    print gcd_steps(8, 13)
    
    d = 24
    p = 3
    print tau(p * d), sum(gcd_steps(i + k * d, p * d) for i in xrange(d) for k in xrange(p) if gcd(i, d) == 1)
    
    for i in (i for i in xrange(d) if gcd(d, i) == 1):
        print 'i %3d' % i,
        for k in xrange(p):
            print (i + k * d, p * d), gcd_steps(i + k * d, p * d),
#            if k == 0:
#                print (i, p * d),
#            elif k == (p - 1) / 2:
#                if i > d / 2:
#                    print (d * p - i - k * d, p * d), 1,
#                else:
#                    print (i + k * d, p * d),
#            elif k > p / 2:
#                print (d * p - i - k * d, p * d), 1,
#            else:
#                print (p * d - i - k * d, i + k * d),
        print ''

    
    d = 252
    # r = rad(n + 1)[-1]
    ph = phi(d + 1)[-1]
    
    p = 2
    print 'd', d, 'phi(d)', ph, 'tau(p*d)', tau(2 * d), tau(3 * d)

#    print sum(gcd_steps(i + k * d, p * d) for i in xrange(d) for k in xrange(p) if gcd(i, d) == 1)
#    print 3 * ph + sum(gcd_steps(2 * d - i, i) + gcd_steps(d + i, d - i) for i in xrange(d) if gcd(i, d) == 1)
#    print 3 * ph + 2 * sum(gcd_steps(2 * d - i, i) for i in xrange(d) if gcd(i, d) == 1)

    print ph + 2 * sum(gcd_steps(i, 2 * d) for i in xrange(d) if gcd(i, d) == 1)
    print sum(gcd_steps(i, 3 * d) for i in xrange(d) if gcd(i, d) == 1)
