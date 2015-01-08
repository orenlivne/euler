'''
============================================================
http://projecteuler.net/problem=66

Consider quadratic Diophantine equations of the form:

x^2 - D*y^2=1

For example, when D=13, the minimal solution in x is 6492 - 131802 = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

32 - 222 = 1
22 - 312 = 1
92 - 542 = 1
52 - 622 = 1
82 - 732 = 1

Hence, by considering minimal solutions in x for D  7, the largest x is obtained when D=5.

Find the value of D  1000 in minimal solutions of x for which the largest value of x is obtained.
============================================================
'''
import itertools as it, numpy as np
from problem064 import divide
from problem065 import cont_convergent
from operator import itemgetter

def cont_expansion(x):
    '''An iterable of a-coefficients of sqrt(x)''s continued fraction expansion. If x is a
    perfect square, returns [].'''
    sx = x ** 0.5
    y = int(sx)
    if sx < y + 1e-10:
        raise StopIteration
    a = (y, 1, y)
    while True:
        yield a
        a = divide(x, sx, a)
        
def pell_solution(D, s=1):
    '''Return the fundamental solution to Pell''s equation, x^2-D*y^2 = s. s must be 1 or -1.'''
    try: return it.dropwhile(lambda (x, y): x * x - D * y * y != s,
                             cont_convergent(it.imap(itemgetter(0), cont_expansion(D)))).next()
    except StopIteration: return (0, 0)  # D is a perfect square

if __name__ == "__main__":
    print np.argmax(map(itemgetter(0), it.imap(pell_solution, xrange(2, 1001)))) + 2  # 661
    print np.argmax(map(itemgetter(0), it.imap(pell_solution, xrange(2, 10001)))) + 2  # 9949
