'''
============================================================
http://projecteuler.net/problem=137

Consider the infinite polynomial series AF(x) = xF1 + x2F2 + x3F3 + ..., where Fk is the kth term in the Fibonacci sequence: 1, 1, 2, 3, 5, 8, ... ; that is, Fk = Fk1 + Fk2, F1 = 1 and F2 = 1.

For this problem we shall be interested in values of x for which AF(x) is a positive integer.

Surprisingly AF(1/2)     =     (1/2).1 + (1/2)2.1 + (1/2)3.2 + (1/2)4.3 + (1/2)5.5 + ...
      =     1/2 + 1/4 + 2/8 + 3/16 + 5/32 + ...
      =     2
The corresponding values of x for the first five natural numbers are shown below.

x    AF(x)
21    1
1/2    2
(132)/3    3
(895)/8    4
(343)/5    5
We shall call AF(x) a golden nugget if x is rational, because they become increasingly rarer; for example, the 10th golden nugget is 74049690.

Find the 15th golden nugget.
============================================================
'''
from itertools import islice, count, dropwhile, ifilter, imap
from problem086 import is_int

def pell_solution4(D):
    '''Generates solutions to x^2-D*y^2 = +-4. D must be 1 (mod 4) and >= 5.'''
    # Calculate the fundamental solution with RHS=-4 by brute force. PQa would have been faster.
    xt, yt = dropwhile(lambda (x, _): not is_int(x), ((D * y * y - 4, y) for y in count(1))).next()
    yield xt, yt
    x0, y0, x1, y1 = 2, 0, xt, yt
    while True:
        x, y = xt * x1 + x0, xt * y1 + y0
        yield x, y
        x0, y0, x1, y1 = x1, y1, x, y
        
golden_nugget = imap(lambda (_, x): (x[0] - 1) / 5, ifilter(lambda (n, (x, _)): n % 2 and x % 5 == 1, enumerate(pell_solution4(5), 1)))
    
def golden_nugget_manual(b1, c1):
    '''A generator of Golden nuggets for a generating function that can be reduced to Pell's
    solution with s=-4. The fundamental solution to c**2-D*b**2 = -4 must be input.''' 
    n, c0, b0 = 2, 2, 0
    while True:
        b, c = b0 + b1, c0 + c1
        if n % 2 and c % 5 == 1: yield (c - 1) / 5
        n, c0, b0, c1, b1 = n + 1, c1, b1, c, b
        
if __name__ == "__main__":
    print islice(golden_nugget_manual(1, 1), 14, 15).next()
    print islice(golden_nugget, 15, 16).next()
    
