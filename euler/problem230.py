'''
============================================================
http://projecteuler.net/problem=230

For any two strings of digits, A and B, we define FA,B to be the sequence (A,B,AB,BAB,ABBAB,...) in which each term is the concatenation of the previous two.

Further, we define DA,B(n) to be the nth digit in the first term of FA,B that contains at least n digits.

Example:

Let A=1415926535, B=8979323846. We wish to find DA,B(35), say.

The first few terms of FA,B are:
1415926535
8979323846
14159265358979323846
897932384614159265358979323846
14159265358979323846897932384614159265358979323846
Then DA,B(35) is the 35th digit in the fifth term, which is 9.

Now we use for A the first 100 digits of pi behind the decimal point:

14159265358979323846264338327950288419716939937510 
58209749445923078164062862089986280348253421170679

and for B the next hundred digits:

82148086513282306647093844609550582231725359408128 
48111745028410270193852110555964462294895493038196 .

Find sum n = 0,1,...,17   10**n x DA,B((127+19n)x7n) .
============================================================
'''
from math import log
from itertools import islice
from problem002 import fibonacci

'''Dynamic-programming to calculate the digit D_{a,b}(n). l = length of all words up to the maximum
n passed to this function.'''
d = lambda a, b, l, n, i: a[i - 1] if n == 0 else (b[i - 1] if n == 1 else \
(d(a, b, l, n - 2, i) if i < l[n - 2] else d(a, b, l, n - 1, i - l[n - 2])))

'''Index of the smallest Fibonacci number greater than ((127+19n)*7**n)/s.''' 
R_LOG_PHI = 1. / log((1 + 5 ** 0.5) * 0.5)
k = lambda N, s: int((log(127 + 19 * N) + N * log(7) + log(5 ** 0.5 / s)) * R_LOG_PHI)

def digits(a, b, n_max):
    '''Return the digit D_{a,b}(n). Assuming the digit sequences a and b are of equal length.'''
    # Cache all relevant Fibonacci word lengths, which are proportional to the Fibonacci numbers
    s = len(a)
    l = map(lambda x: s * x, islice(fibonacci(), k(n_max, s) + 1))
    for n in xrange(n_max): yield d(a, b, l, k(n, s), (127 + 19 * n) * 7 ** n)

'''Join digits (same as evaluating sum 10^n * digit(n) over the requested n-range.'''
sum_digits = lambda a, b, n_max: ''.join(map(str, reversed(list(digits(a, b, n_max)))))

if __name__ == "__main__":
    a = map(int, '1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')
    b = map(int, '8214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196')
    print sum_digits(a, b, 18)
