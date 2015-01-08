'''
============================================================
http://projecteuler.net/problem=118

Using all of the digits 1 through 9 and concatenating them freely to form decimal integers, different sets can be formed. Interestingly with the set {2,5,47,89,631}, all of the elements belonging to it are prime.
How many distinct sets containing each of the digits one through nine exactly once contain only prime elements?
============================================================
'''
import itertools as it
from math import log10, ceil
from problem007 import primes
from problem027 import is_prime

P = primes('lt', int(98765432 ** 0.5) + 1)
is_p = lambda x: is_prime(x, P)

'''Digits = set of remaining digits. n_min = maximum number in set so far.'''
# num_prime_sets = lambda digits, n_min: sum(num_prime_sets(digits - set(map(int, str(x))), x) for x in 
#                                            it.ifilter(is_p, xrange(n_min + 1, min(100000000, int(''.join(sorted(map(str, digits), reverse=True))) + 1)))) if digits else 1

def num_prime_sets(digits, n_min, n_max=None):
    if not digits: return 1    
    digits_str = map(str, digits)
    eligible = (lambda x: x > n_min and x <= n_max and is_p(x)) if n_max else (lambda x: x > n_min and is_p(x))
    max_digits = min(8, len(digits))
    if n_max: max_digits = min(max_digits, int(ceil(log10(n_max))))
    x_primes = it.ifilter(eligible, (int(''.join(x)) for r in xrange(1, max_digits + 1) for x in it.permutations(digits_str, r)))
    return sum(num_prime_sets(digits - set(map(int, str(x))), x) for x in x_primes)

if __name__ == "__main__":
    print num_prime_sets(set(range(1, 10)), 0, 9876)
    
