'''
============================================================
http://projecteuler.net/problem=190

Let Sm = (x1, x2, ... , xm) be the m-tuple of positive real numbers with x1 + x2 + ... + xm = m for which Pm = x1 * x22 * ... * xmm is maximised.

For example, it can be verified that [P10] = 4112 ([ ] is the integer part function).

Find sum [Pm] for 2 <= m <= 15.
============================================================
'''

if __name__ == "__main__":
    print sum(int(reduce(lambda x, y: x * y, (((2.*k) / (m + 1)) ** k for k in xrange(1, m + 1)))) for m in xrange(2, 16))
