'''
============================================================
http://projecteuler.net/problem=323

Let y0, y1, y2,... be a sequence of random unsigned 32 bit integers
(i.e. 0 <= yi < 232, every value equally likely).

For the sequence xi the following recursion is given:
x0 = 0 and
xi = xi-1 | yi-1, for i > 0. ( | is the bitwise-OR operator)
It can be seen that eventually there will be an index N such that xi = 232 -1 (a bit-pattern of all ones) for all i >= N.

Find the expected value of N. 
Give your answer rounded to 10 digits after the decimal point.
============================================================
'''
def expected_N(k, tol):
    s, n = 0, 0
    while True:
        n += 1
        term = n * ((1 - 0.5 ** n) ** k - (1 - 0.5 ** (n - 1)) ** k)
        s += term
        if term < tol: return s 

if __name__ == "__main__":
    for k in xrange(1,33): print '%d %.10f' % (k, expected_N(k, 1e-11))
