'''
============================================================
http://projecteuler.net/problem=200

We shall define a sqube to be a number of the form, p2q3,
where p and q are distinct primes.
For example, 200 = 5**2*2**3 or 120072949 = 23**2*61**3.

The first five squbes are 72, 108, 200, 392, and 500.

Interestingly, 200 is also the first number for which you
cannot change any single digit to make a prime; we shall
call such numbers, prime-proof. The next prime-proof sqube
which contains the contiguous sub-string "200" is 1992008.

Find the 200th prime-proof sqube containing the contiguous
sub-string "200".
============================================================
'''
import itertools as it
from math import ceil
from euler.problem007 import primes
from euler.problem146 import isp

TARGET = '200'
DIGITS = map(str, xrange(10))
NON_ZERO_DIGITS = map(str, xrange(1, 10))

def is_prime_proof_and_contains_target(x):
    s = str(x)
    return TARGET in s and \
        not any(isp(int(s[:i] + d + s[i + 1:]))
                   for i in xrange(len(s)) 
                   for d in (NON_ZERO_DIGITS if i == 0 else DIGITS) if d != s[i])

def list_in_range(lst, low, high):
    '''Sub-list of lst with elements in [low,high]. Convert to long integers.'''
    return it.imap(long, it.dropwhile(lambda x: x < low, it.takewhile(lambda x: x <= high, lst)))

def int_le(x):
    is_int = abs(x - round(x)) < 1e-5
    return int(round(x)) if is_int else int(x)

def sqcubes(a, b):
    '''All sqcubes in [a,b].'''
    q_max = int_le((b / 4) ** (1. / 3.))
    prime_list = primes('lt', max(q_max, int_le((b / 8) ** (1. / 2.))) + 1)
    return ((p, q, p ** 2L * q ** 3L)
            for q in list_in_range(prime_list, 2, q_max)
            for p in list_in_range(prime_list,
                                   max(2, int(ceil((a / q ** 3) ** 0.5))), int_le((b / q ** 3) ** 0.5))
            if p != q)

def nth_sqube_containing_target(n):
    a, b, found = 2L, 1000L, 0
    all_solutions = []
    while found < n:
        solutions = sorted(filter(lambda x: is_prime_proof_and_contains_target(x[2]), sqcubes(a, b)),
                           key=lambda x: x[2])
        a, b = b + 1, 4 * b
        all_solutions += solutions
        found = len(all_solutions)
        #print a, ':', b, 'found so far', found, solutions
    return sorted(all_solutions, key=lambda x: x[2])[n - 1]

if __name__ == "__main__":
    print nth_sqube_containing_target(200)
