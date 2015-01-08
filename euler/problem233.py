'''
============================================================
http://projecteuler.net/problem=233

Let f(N) be the number of points with integer coordinates that are on a circle passing through (0,0), (N,0),(0,N), and (N,N).
It can be shown that f(10000) = 36.
What is the sum of all positive integers N <= 1011 such that f(N) = 420?
============================================================
'''
import itertools as it, numpy as np
from math import log
from problem007 import primes
from problem012 import Primes

'''Return all ordered partitions of subsets of the list a of distinct elements.'''
partitions_of_distinct = lambda a: [[list(s)] + y for i in xrange(1, len(a)) for s in it.combinations(a, i) for y in partitions_of_distinct(sorted(set(a) - set(s)))] + [[a]]
'''Return all ordered partitions of subsets of the list a. Does not have to have distinct elements. For convenience, sorted by lexicographic order, but that''s not really necessary for our application.'''
partitions = lambda a: sorted(set([tuple(tuple(a[i] for i in part) for part in partition) for partition in partitions_of_distinct(range(len(a)))]))  # @UndefinedVariable @UnusedVariable

'''Set/list element product.'''
prod = lambda a: reduce(lambda x, y:x * y, a, 1)

def p_prime(N, P):
    '''Is N=p[0]^a0*...*p[k]^ak with ai >= 0?'''
    for p in P:
        if N == 1: return True
        while N % p == 0: N /= p
    return N == 1

def prime_factors(B, primes=None):
    '''List of non-distinct primes factors of B(=F/4), B>=1.'''
    for p in (primes if primes is not None else Primes()):
        while B % p == 0:
            yield p
            B /= p
        if B == 1: break

'''Sum of all n = p[0]^a0*...*p[k]^ak <= N with ai >= 0.'''
g = lambda N, P: sum(n for n in xrange(1, N + 1) if p_prime(n, P))

'''Primes that are not 1(mod 4).'''
p_primes = lambda L, include_two: ([2] if include_two else []) + filter(lambda x: x % 4 == 3, primes('lt', L + 1))
    
'''A generator of primes that are 1 (mod 4).'''
primes1 = lambda: it.ifilter(lambda x: x % 4 == 1, it.imap(long, Primes()))

'''Primes that are not 3(mod 4).'''
not_p_primes = lambda L, include_two: ([2] if not include_two else []) + filter(lambda x: x % 4 == 1, it.imap(long, primes('lt', L + 1)))

def sum_r(L, include_two):
    '''Sum of r = p[0]^a0*...*p[k]^ak <= L with p's = primes = 3(mod 4) <= N. Uses a sieve
    to calculate the complement of this sum.'''
    s = np.array([True] * (L + 1), dtype=bool); s[0] = False
    for p in not_p_primes(L, include_two): s[p::p] = False
    return sum(map(long, np.where(s)[0]))

def q_combos(q_set, b, L):
    '''Returns all combinations (q1,...,qk) such that qi are in q_set, q1 < ... < qk and prod(qi^bi) <= L.'''
    q1_max = L ** (1. / sum(b))
    q1_set = it.takewhile(lambda x: x <= q1_max, q_set)
    if len(b) == 1:
        return [[q1] for q1 in q1_set]
    else:
        result = []
        for k, q1 in enumerate(q1_set):
            q1_element = [q1]
            result += [q1_element + rest for rest in q_combos(q_set[k + 1:], b[1:], float(L) / q1 ** b[0])]
        return result
            
def sum_f(F, L):
    '''Returns the sum of all n <= L such that f(n)=F.'''
    if F % 4: return 0
    B_factors, count, log_L = list(prime_factors(F / 4)), 0, log(L)  # Call B = F/4  in the docs hereafter
    # q-primes = 1 (mod 4). p-primes = 3 (mod 4). First store all possible q-primes that can
    # fit in the decomposition of B = F/4 
    q_primes = list(it.islice(primes1(), len(B_factors)))
    # Partition B into all possible (2*b1+1)*...*(2*br+1)
    for partition in partitions(B_factors):
        B = [prod(x) for x in partition]
        if all(x % 2 == 1 for x in B):
            B = [x / 2 for x in B]
            # For each such partition, check if prod(q_i^bi) <= 1 with the smallest possible q's
            # Here we always order the primes such that q1 < q2 < ... < qr.
            if sum(log(x) * b for x, b in it.izip(q_primes, B)) <= log_L:
                # The maximum possible q-prime q_max is such that prod(q_i^bi) <= L even with the
                # smallest primes preceding qr = q_max in this product
                q_tilde = prod(x ** b for x, b in it.izip(q_primes, B[:-1]))
                q_max = int((float(L) / q_tilde) ** (1. / B[-1]))
                qb = list(it.takewhile(lambda x: x <= q_max, primes1()))
                # Loop over all selections of q1,...,qr. Let q = prod(q_i^bi).
                # Find all r's such that
                # N = 2 r q (if N even, with r composed of 2 and p-primes) or
                # N = r q (if N odd, with r composed of p-primes).
                # Sum all such r's, and multiply by 2 q (even N) or q (odd N) 
                for Q in q_combos(qb, B, L):  # it.combinations(qb, len(B)):
                    if sum(log(x) * b for x, b in it.izip(Q, B)) <= log_L:
                        q = prod(x ** b for x, b in it.izip(Q, B))
                        L1 = int(float(L) / q)
                        L2 = int(float(L) / (2 * q))
                        n1 = sum_r(L1, False)
                        n2 = sum_r(L2, True)
                        count += (q * n1 + 2 * q * n2)
    return count

if __name__ == "__main__":
    print sum_f(420, 10 ** 11)
