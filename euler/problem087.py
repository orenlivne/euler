'''
============================================================
http://projecteuler.net/problem=87

The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28. In fact, there are exactly four numbers below fifty that can be expressed in such a way:

28 = 2^2 + 2^3 + 2^4
33 = 3^2 + 2^3 + 2^4
49 = 5^2 + 2^3 + 2^4
47 = 2^2 + 3^3 + 2^4

How many numbers below fifty million can be expressed as the sum of a prime square, prime cube, and prime fourth power?
============================================================
'''
from problem007 import primes
from itertools import product, imap

def sum_till_ge(iterable, limit):
    '''Sum the iterates produced by iterable until the sum >= limit. Return that sum. Avoids overflow.'''
    s = 0
    for x in iterable:
        s += x
        if s >= limit: return s
    return s

'''Returns the number of numbers < N expressible as p_1^2 + ... + p_{k-1}^k where all p_i are prime.'''
num_sums = lambda N, k: len(set(filter(lambda x: x < N, imap(lambda x: sum_till_ge(x, N), product(*(map(lambda p: p ** l, primes('lt', int((N - (2 ** (k + 1) - 4 - 2 ** l)) ** (1.0 / l)) + 1)) for l in xrange(2, k + 1)))))))

if __name__ == "__main__":
    print num_sums(50000000, 4)  # 1097343
    print num_sums(5000000, 5)  # 898390
