'''
============================================================
http://projecteuler.net/problem=214

Let phi be Euler's totient function, i.e. for a natural number n, phi(n) is the number of k, 1 <= k <= n, for which gcd(k,n) = 1.

By iterating phi, each positive integer generates a decreasing chain of numbers ending in 1.
E.g. if we start with 5 the sequence 5,4,2,1 is generated.
Here is a listing of all chains with length 4:

5,4,2,1
7,6,2,1
8,4,2,1
9,6,2,1
10,4,2,1
12,4,2,1
14,6,2,1
18,6,2,1
Only two of these chains start with a prime, their sum is 12.

What is the sum of all primes less than 40000000 which generate a chain of length 25?
============================================================
'''
from problem007 import primes
from problem070 import phi

def chain_len(f, x, max_len):
    count = 1
    while x > 1 and count <= max_len: x, count = f[x], count + 1
    return count if count <= max_len else -1

def sum_primes_of_len(N, L):
    p = primes('lt', N)
    print 'N', N, '#primes', len(p)
    f = phi(N, p)
    print 'phi', f
    s = 0
    for k, x in enumerate(long(x) for x in p):
        l = chain_len(f, x, L)
        if not (k % 10000): print x, l
        if l == L: s += x
    return s
    # return sum(long(x) for x in p if chain_len(f, x, L) == L)

if __name__ == "__main__":
    print sum_primes_of_len(4 * 10 ** 6, 25)
    print sum_primes_of_len(4 * 10 ** 7, 25)
