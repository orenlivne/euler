'''
============================================================
http://projecteuler.net/problem=71

Consider the fraction, n/d, where n and d are positive integers. If nd and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d  8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d  1,000,000 in ascending order of size, find the numerator of the fraction immediately to the left of 3/7.
============================================================
'''
from problem005 import gcd

def max_frac((nt, dt), D):  # D>=3
    rt, (n_max, d_max), r_max = float(nt) / dt, (0, 1), 0.
    for d in xrange(4, D):
        if d == dt: continue
        m = d * r_max
        for n in xrange(int(rt * d), 0, -1):
            if n < m: break
            if gcd(d, n) == 1:
                n_max, d_max, r_max = n, d, float(n) / d
                break
    return n_max, d_max
                
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print max_frac((3, 7), 1000000)
