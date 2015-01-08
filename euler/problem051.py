'''
============================================================
http://projecteuler.net/problem=51

By replacing the 1st digit of *3, it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family.
============================================================
'''
from problem049 import primes_in_range
import itertools as it, numpy as np
from euler.problem037 import is_prime

'''Return the smallest number in a k-prime family with at most max_digits digits.'''
smallest_in_family = lambda k, max_digits: it.chain.from_iterable(_smallest_in_family(k, d) for d in xrange(2, max_digits + 1)).next()

'''All subsets of {0,...,n-1}.'''
all_subsets = lambda n: it.chain.from_iterable(it.combinations(range(n), d) for d in xrange(n + 1))

'''All subsets of {0,...,n-1} except the empty set.'''
all_nonempty_subsets = lambda n: it.chain.from_iterable(it.combinations(range(n), d) for d in xrange(1, n + 1))

def _smallest_in_family(k, d):
    '''Return the smallest number in a k-prime family with d >= 2 digits.'''
    # print 'k', k, 'd', d
    p = set(primes_in_range(10 ** (d - 1), 10 ** d))
    all_digits = set(range(d))  # All digits that may be stars. 0=left-most. Last cannot be a star.
    # print 'all_digits', all_digits, 'p', p
    for stars in map(np.array, all_nonempty_subsets(d - 1)):
        fixed = np.array(list(all_digits - set(stars)))
        # print 'stars', stars, 'fixed', fixed
        # print [substitutes(n, d) if n in fixed else [0] for n in xrange(d)]
        for combo in it.ifilter(lambda x: x > 0, it.imap(lambda x: _fam_result(np.array(x), stars, k, p),
                                                         it.product(*(substitutes(n, d) if n in fixed else [0] for n in xrange(d))))):  # @UndefinedVariable
            # print 'combo', combo
            yield combo

'''Possibilities for replacing digit number n in a d-digit #.'''
substitutes = lambda n, d: range(1, 10) if n == 0 else (range(10) if n < d - 1 else [1, 3, 7, 9]) 

'''To eliminate many re-allocations in _fam_result().'''
fam = np.zeros((10,), dtype=np.uint)

def _fam_result(num, stars, k, p):
    '''If num is a member of a k- p-member family when stars' digits are replaced with the same digit,
    return the min in the family, otherwise return -1.'''
    # print num, stars, k, p
    good, bad, ugly = 0, 0, 10 - k
    for x in xrange(10):
        a = num
        if stars.size:
            a[stars] = x
        # print map(str, a)
        b = int(''.join(map(str, a)))
        # print '\tb', b
        if b in p:
            fam[good] = b
            good += 1
        else:
            bad += 1
            if bad > ugly:
                return -1
    # print good
    return min(fam[:good])

def akino_solution(k):
    digits = '0123456789'
    for D in it.count(3):  # total no of digits in number
        DM = D - 1
        for x in xrange(1, DM):  # no of fixed digits
            all_xs = ['x'] * DM
            for fix_pos in it.combinations(range(0, DM), x):  # position of fixed digits
                for last in '1379':
                    for fix_dig in it.product(digits, repeat=x):
                        n = all_xs + [last]
                        for i in xrange(x):
                            n[fix_pos[i]] = fix_dig[i]
                        if n[0] != '0':
                            num = ''.join(n)
                            begin = 0 if 0 in fix_pos else 1
                            lst = [is_prime(int(num.replace('x', str(f)))) for f in xrange(begin, 10)]
                            # Might be improved by stopping if there are >= 3 non-primes
                            if lst.count(True) >= k:
                                return min(int(num.replace('x', str(f))) for f in xrange(begin, 10))
                            
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    # print smallest_in_family(6, 3)
    # print smallest_in_family(7, 5)
    import time

    start = time.time()
    print akino_solution(8)
    print time.time() - start, 'sec'

    start = time.time()
    print smallest_in_family(8, 6)
    print time.time() - start, 'sec'
