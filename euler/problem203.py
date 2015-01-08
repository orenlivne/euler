'''
============================================================
http://projecteuler.net/problem=203

The binomial coefficients nCk can be arranged in triangular form, Pascal's triangle, like this:

1    
1        1    
1        2        1    
1        3        3        1    
1        4        6        4        1    
1        5        10        10        5        1    
1        6        15        20        15        6        1    
1        7        21        35        35        21        7        1
.........
It can be seen that the first eight rows of Pascal's triangle contain twelve distinct numbers: 1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 21 and 35.

A positive integer n is called squarefree if no square of a prime divides n. Of the twelve distinct numbers in the first eight rows of Pascal's triangle, all except 4 and 20 are squarefree. The sum of the distinct squarefree numbers in the first eight rows is 105.

Find the sum of the distinct squarefree numbers in the first 51 rows of Pascal's triangle.
============================================================
'''
from itertools import count, islice
from problem007 import primes
import numpy as np

def binom():
    b = [1L]
    yield list(b)
    for n in count(1):
        a = list(b)
        for i in xrange(n - 1): b[i] = a[i] + a[i + 1]
        b.insert(0, 1L)
        yield b[:n + 1]

def sum_sf(N):
    b = list(islice(binom(), 0, N))
    d = set([y for x in b for y in x])
    p = map(lambda x: long(x * x), primes('lt', int(N + 1) + 1))
    return sum(np.array(list(d))[np.array(map(lambda x: all(x % y for y in p), d))])

if __name__ == "__main__":
    print sum_sf(8)  # 105
    print sum_sf(50)  # 34029210557338
    print sum_sf(100)  # 5014910710588270546867579871
