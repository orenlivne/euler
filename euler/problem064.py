'''
============================================================
http://projecteuler.net/problem=64

All square roots are periodic when written as continued fractions and can be written in the form:

N = a0 +    
1
     a1 +    
1
          a2 +    
1
               a3 + ...
For example, let us consider 23:

If we continue we would get the following expansion:

The process can be summarised as follows:

It can be seen that the sequence is repeating. For conciseness, we use the notation 23 = [4;(1,3,1,8)], to indicate that the block (1,3,1,8) repeats indefinitely.

The first ten continued fraction representations of (irrational) square roots are:

2=[1;(2)], period=1
3=[1;(1,2)], period=2
5=[2;(4)], period=1
6=[2;(2,4)], period=2
7=[2;(1,1,1,4)], period=4
8=[2;(1,4)], period=2
10=[3;(6)], period=1
11=[3;(3,6)], period=2
12= [3;(2,6)], period=2
13=[3;(1,1,1,1,6)], period=5

Exactly four continued fractions, for N  13, have an odd period.

How many continued fractions for N  10000 have an odd period?
============================================================
'''
from itertools import count, ifilter, imap
from math import modf

def sqrt_period(x):
    '''Returns the continued-fraction period of sqrt(x).'''
    sx = x ** 0.5
    y = int(sx)
    if sx < y + 1e-10:
        return 0
    a = (y, 1, y)
    a = divide(x, sx, a)  # a = (a1,b1,c1)
    b = a
    for n in count(1):
        b = divide(x, sx, b)  # b = (a_{n+1},b_{n+1},c_{n+1})
        if b == a:
            return n

def divide(x, sx, (a, b, c)):
    '''One iteration of continued-fraction division.'''
    f, i = modf(b / (sx - c))
    a1, b1 = int(i), (x - c * c) / b
    c1 = int(round(sx - b1 * f))
    return a1, b1, c1

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print sqrt_period(23)
    print sum(1 for _ in ifilter(lambda n: n > 0 and n % 2 == 1, imap(sqrt_period, xrange(2, 10001))))
