'''
============================================================
http://projecteuler.net/problem=21

Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a  b, then a and b are an amicable pair and each of a and b are called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, itertools
from problem007 import primes
#from euler.problem005 import gcd

class DCalculator(object):
    '''Calculates d[1]..d[n-1].'''
    def __init__(self, n):
        self._n = n
        self._d = np.zeros((n,), dtype=np.uint) # d-values cache
        self._p = primes('lt', n) # Prime list
        self._d[self._p] = 1 # B.C.
        self._d[1] = 1
        
    def d(self, a):
        #print 'd[%d]' % (a,)
        if a == 0:
            return 0
        if not self._d[a]: # Not in cache, invoke dynamic programming
            p, k = self._smallest_prime_factor(a)
            #print '\tFactor:', p, ',', k
            pk = p ** k
            b = a / pk
            self._d[a] = (pk - 1) / (p - 1) if b == 1 else \
            (p * pk - 1) / (p - 1) * (self.d(b) + b) - pk * b # (DP)
        #print '\td[%d] = %d' % (a, self._d[a])
        return self._d[a] # In cache already
    
    def divisor_sum(self):
        '''Returns d[x] for all x < n.'''
        return np.array([self.d(x) for x in xrange(self._n)])

    def _d2(self):
        '''Returns d[d[x]] (0 or, if d[x] is out of range).'''
        d2 = self.divisor_sum()
        # Omit a = b pairs (perfect numbers)
        d2[np.where(d2 == np.arange(self._n))[0]] = 0
        d2[np.where(d2 >= self._n)[0]] = 0
        d2 = d2[d2]
        return d2
    
    def amicable(self):
        '''Returns the list of amicable numbers < n.'''
        a = np.arange(2, self._n)
        return a[np.where(self._d2()[a] == a)[0]]
    
    def _smallest_prime_factor(self, a):
        '''Returns p, multiplicity of p.'''
        for p in self._p:
            if a % p == 0: break
        count = 1
        a /= p
        while a % p == 0:
            count += 1
            a /= p
        return p, count

def factors(n):
    '''Prime factorization. Taken from http://glowingpython.blogspot.com/2011/07/prime-factor-decomposition-of-number.html'''
    result = []
    # test 2 and all odd numbers
    for i in itertools.chain([2], xrange(3, n + 1, 2)):
        s = 0
        while n % i == 0:
            n /= i
            s += 1
        result.extend([i] * s) #avoid another for loop
        if n == 1: return result

def powerset(iterable): # Except the entire set
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in xrange(len(s) + 1))
                            

subsets = lambda s:map(set, set(powerset(s)))

def divisor_sum_bf(a):
    '''d[a], calculated using brute force.'''
    if a == 0: return 0
    elif a == 1: return 1
    else: return sum(set(reduce(lambda x, y: x * y, x, 1) for x in list(powerset(factors(a)))) - set([a]))

if __name__ == "__main__":
    #print brent(220)
    n = 10000
    D = DCalculator(n)
    d = D.divisor_sum() 
    b = max(d)
    print b

    D = DCalculator(b + 1)
    dall = D.divisor_sum()
    a = D.amicable()
    a = a[np.where(a < n)[0]]
    print 'amicable', a 
    print sum(a)
#    import doctest
#    doctest.testmod()
