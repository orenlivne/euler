'''
============================================================
http://projecteuler.net/problem=49

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
============================================================
'''
from problem037 import is_prime
import itertools as it

primes_in_range = lambda low, high: filter(is_prime, xrange(low, high))
perms = lambda x : set(map(int, map(''.join, it.permutations(str(x)))))  # asorted set of distinct permuatations of x's digits 

def all_triplets():
    '''Yield all triplets among 4-digit numbers.'''
    primes = primes_in_range(1000, 10000)  # Sorted
    prime_set = set(primes)  # Not guaranteed to be sorted
    visited = dict((x, False) for x in primes)
    
    for x in primes:
        if not visited[x]:
            p = filter(prime_set.__contains__, perms(x))
            for y in p:
                visited[y] = True
            if len(p) >= 3:
                for triplet in triplets(sorted(p)):
                    yield triplet
                    
def triplets(p):
    '''Yield all triplets within the sorted list p.'''
    for i in xrange(len(p)):
        x = p[i]
        for j in xrange(i + 1, len(p)):
            y = p[j]
            z = 2 * y - x
            if z in p:
                yield int(''.join(map(str, [x, y, z])))

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print list(all_triplets())
