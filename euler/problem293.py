'''
============================================================
http://projecteuler.net/problem=293

An even positive integer N will be called admissible, if it is a power of 2 or its distinct prime factors are consecutive primes.
The first twelve admissible numbers are 2,4,6,8,12,16,18,24,30,32,36,48.

If N is admissible, the smallest integer M > 1 such that N+M is prime, will be called the pseudo-Fortunate number for N.

For example, N=630 is admissible since it is even and its distinct prime factors are the consecutive primes 2,3,5 and 7.
The next prime number after 631 is 641; hence, the pseudo-Fortunate number for 630 is M=11.
It can also be seen that the pseudo-Fortunate number for 16 is 3.

Find the sum of all distinct pseudo-Fortunate numbers for admissible numbers N less than 109.
============================================================
'''
from itertools import dropwhile, count
from problem007 import primes
from problem146 import is_probable_prime

not_probable_prime = lambda x: not is_probable_prime(x)
PRIMES = map(long, primes('lt', 100))  # First 100 primes enough for any limit < 1e36

def admissible_lt(limit, prime_index, n_prev):
    '''Generator of admissible numbers < N.'''
    # Enumerate admissible numbers by 2^k1 3^k2 ... pm^km by a DFS
    p = PRIMES[prime_index]
    n = n_prev * p
    while n < limit:
        yield n
        for k in admissible_lt(limit, prime_index + 1, n): yield k
        n *= p

'''Distinct pseudo-fortunate numbers < N. Brute-force search over m for the smallest prime n+m for
each admissible n.''' 
distinct_pf_lt = lambda limit: set(dropwhile(not_probable_prime, count(n + 2)).next() - n for n in admissible_lt(limit, 0, 1))

if __name__ == "__main__":
    print sum(distinct_pf_lt(10 ** 9))
