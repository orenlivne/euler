'''
============================================================
Let S = {2, 3, 5, ..., 4999} be the set of prime numbers less than 5000.

Find the number of subsets of S, the sum of whose elements is a prime number.
Enter the rightmost 16 digits as your answer.
============================================================
'''
from itertools import islice
from problem007 import primes

def num_prime_subsets(S_lim, t):
    '''Return the number of of subsets of S (the set of all primes < S_lim),
    the sum of whose elements is a prime number. The result is returned modulo t.'''
    S = primes('lt', S_lim)
    # w[s] = how many subsets have sum s
    n = sum(S) + 1 
    w = [0L] * n
    # Set Initial condition. Include the empty set - convenient for DP.
    w[0] += 1L; w[S[0]] += 1L
    # DP over S elements
    for r in islice(S, 1, None):
        w = [(w[s] + (w[s - r] if s >= r else 0L)) % t for s in xrange(n)]
    return sum(w[s] for s in primes('lt', n)) % t

# from itertools import  combinations
# from euler.problem058 import is_prime
# def num_prime_subsets_bf(S_lim, t):
#     S = primes('lt', S_lim)
#     for s in (s for k in xrange(len(S) + 1) for s in combinations(S, k) if is_prime(sum(s))):
#         print s, sum(s)
#     return sum(1L for k in xrange(len(S) + 1) for s in combinations(S, k) if is_prime(sum(s))) % t

if __name__ == "__main__":
    print num_prime_subsets(5000, 10 ** 16L)
    
