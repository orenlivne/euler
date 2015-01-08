'''
============================================================
http://projecteuler.net/problem=158

Taking three different letters from the 26 letters of the alphabet, character strings of length three can be formed.
Examples are 'abc', 'hat' and 'zyx'.
When we study these three examples we see that for 'abc' two characters come lexicographically after its neighbour to the left.
For 'hat' there is exactly one character that comes lexicographically after its neighbour to the left. For 'zyx' there are zero characters that come lexicographically after its neighbour to the left.
In all there are 10400 strings of length 3 for which exactly one character comes lexicographically after its neighbour to the left.

We now consider strings of n <= 26 different characters from the alphabet.
For every n, p(n) is the number of strings of length n for which exactly one character comes lexicographically after its neighbour to the left.

What is the maximum value of p(n)?
============================================================
'''
import numpy as np, itertools as it

p_bf = lambda s, n: sum(1 for a in it.chain.from_iterable(it.permutations(a) for a in it.combinations(xrange(s), n)) if len(np.where(np.diff(a) > 0)[0]) == 1)  # @UnusedVariable

def x_bf(s, n, k):
    x = np.zeros((s,), dtype=np.long)
    for a in (a for a in it.chain.from_iterable(it.permutations(a) for a in it.combinations(xrange(s), n)) if len(np.where(np.diff(a) > 0)[0]) == k):  # @UnusedVariable
        x[a[-1]] += 1
    return x

def zero_occurrences(s):
    '''Return an array of # strings of length n from alphabet of size s with zero increase occurrences.'''
    x = np.zeros((s + 1, s), dtype=long)
    x[1] = 1  # Initial condition
    for n in xrange(2, s + 1):  # Dynamic programming on string length
        x[n] = x[n - 1]
        for i in xrange(s - 2, n - 2, -1): x[n, i] += x[n, i + 1]
    # Shift left
    for n in xrange(2, s + 1):
        x[n, 0:s - n + 1] = x[n, n - 1:s]
        x[n, s - n + 1:] = 0
    return x

def one_occurrence(s):
    '''Return an array of # strings of length n from alphabet of size s with one increase occurrence.'''
    y = np.zeros((s + 1, s + 1, s), dtype=long)  # Initial conditions at s=1, (n=1,s>=2) already set
    for t in xrange(1, s + 1):  # Dynamic programming on alphabet size
        x = zero_occurrences(t)
        for n in xrange(2, t + 1):
            y[t, n, t - 1] = sum(x[n - 1, 1:t])  # Initial condition #2
            for i in xrange(t - 2, -1, -1): y[t, n, i] = y[t, n, i + 1] + y[t - 1, n - 1, i] - x[n - 1, i + 1]
    return y[s]

def p(s):
    '''number of strings of length n for which exactly one character comes lexicographically after its neighbour to the left,
    for n = 1..s.'''
    y = one_occurrence(s)
    return np.array([sum(y[n, :]) for n in xrange(1, s + 1)], dtype=long)

if __name__ == "__main__":
    print max(p(26))
    
# Testing
#     for s in [5]:  # it.chain(xrange(3, 5), [26]):
#         print 's', s
#         for n in ([3] if s == 26 else xrange(1, s + 1)):
#             x = x_bf(s, n, 0)
#             y = x_bf(s, n, 1)
#             print n, x, y, sum(x), sum(y), p_bf(s, n)
