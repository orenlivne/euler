'''
============================================================
http://projecteuler.net/problem=113

Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

As n increases, the proportion of bouncy numbers below n increases such that there are only 12951 numbers below one-million that are not bouncy and only 277032 non-bouncy numbers below 1010.

How many numbers below a googol (10100) are not bouncy?
============================================================
'''
import numpy as np, scipy.special

def num_non_bouncy(N):
    '''Return the number of non-bouncy numbers < 10**N.'''
    c = [int(round(scipy.special.binom(n + 8, n))) for n in xrange(1, N + 1)]
    p = np.cumsum(c)
    q = np.cumsum(p)
    return p[-1] + q[-1] - 9 * N

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print num_non_bouncy(100)
