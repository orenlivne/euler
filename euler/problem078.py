'''
============================================================
http://projecteuler.net/problem=78

Let p(n) represent the number of different ways in which n coins can be separated into piles. For example, five coins can separated into piles in exactly seven different ways, so p(5)=7.

OOOOO
OOOO   O
OOO   OO
OOO   O   O
OO   OO   O
OO   O   O   O
O   O   O   O   O
Find the least value of n for which p(n) is divisible by one million.
============================================================
'''
import itertools as it

def num_ways(n, modulus):
    '''Return the number of ways to write each 0<=x<n as a sum of primes.'''
    w = [1] + [0] * (n - 1)
    for p in xrange(1, n + 1):
        for y in xrange(p, n): w[y] = (w[y] + w[y - p]) % modulus
        # print p, w
    print w
    return w

def first_num(modulus, criterion, W, n_min):
    n = n_min(W)
    while True:
        try:
            print n
            return it.dropwhile(lambda (_, w): criterion(w, W), enumerate(num_ways(n, modulus))).next()[0]
        except StopIteration:
            n *= 2

#-----------------------
# 26 Apr 2009 01:46 am wakkadojo
# This took me hours. Eventually, thanks to the internet, I learned the recursion relation
# 
# p(n) = p(n-1)+p(n-2)-p(n-5)-p(n-7)+...
#      = sum k(-1)k/2p(n-ak)
# 
# where ak are the generalized pentagonal numbers.
# 
# Runs in 30 seconds on a 1.6GHz pentium-m.
def extend(pent):
    n = len(pent) / 2 + 1
    return pent + [ n * (3 * n - 1) / 2, n * (3 * n + 1) / 2 ]

def next_p(p, pent):
    l = len(p)
    if l > pent[len(pent) - 1]: 
        pent = extend(pent)
    temp, sgn = 0, 1
    for i in xrange(len(pent)):
        if pent[i] > l: break
        else: temp += sgn * p[l - pent[i]]
        if i % 2 == 1: sgn = -sgn 
    p.append(temp)
    return p, pent

def first_num_wakkadojo(modulus):
    pent = [1, 2]
    p = [1, 1, 2]  # p(0) =(def)= 1. p = cache of #ways
    while p[-1] % modulus:
        p, pent = next_p(p, pent)
    return len(p) - 1

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print first_num_wakkadojo(modulus=10 ** 6)
    # print first_num(10, lambda w, W: w != W, 0, lambda W: 100)
#     print first_num(100, lambda w, W: w != W, 0, lambda W: 100)
#     print first_num(1000, lambda w, W: w != W, 0, lambda W: 100)
#     print first_num(10000, lambda w, W: w != W, 0, lambda W: 100)
#     print first_num(100000, lambda w, W: w != W, 0, lambda W: 100)
#     print first_num(1000000, lambda w, W: w != W, 0, lambda W: 100)
