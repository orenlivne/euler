'''
============================================================
http://projecteuler.net/problem=134

Consider the consecutive primes p1 = 19 and p2 = 23. It can be verified that 1219 is the smallest number such that the last digits are formed by p1 whilst also being divisible by p2.

In fact, with the exception of p1 = 3 and p2 = 5, for every pair of consecutive primes, p2  p1, there exist values of n for which the last digits are formed by p1 and n is divisible by p2. Let S be the smallest of these values of n.

Find  S for every pair of consecutive primes with 5  p1  1000000.
============================================================
'''
from math import log, ceil
from problem007 import primes

def extended_gcd(a, b):
    '''Returns the coefficients x,y of a*x + b*y = gcd(a,b). Extended Euclid''s algorithm.'''
    x, y, lastx, lasty = 0L, 1L, 1L, 0L
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        x, y, lastx, lasty = lastx - q * x, lasty - q * y, x, y
    return lastx, lasty

def s_pair(p1, p2):
    k = int(ceil(log(p1) / log(10)))
    ten_k = 10 ** k
    b, c = p2 - p1, ten_k % p2
    # Basically, I re-invented here the solution provided by the Chinese Remainder Theorem
    # to the system a (mod 10^k)=p1, a (mod p2)=0.
    y, _ = extended_gcd(b, p2)
    a, _ = extended_gcd(c * y, p2)
    if a < 0: a += p2
    return ten_k * a + p1

def sum_s(N):
    p_list, s = map(int, primes('lt', int(1.05 * N))[2:]), 0
    for i, p1 in enumerate(p_list[:-1]):
        if p1 > N: break
        s += s_pair(p1, p_list[i + 1])
    return s 

if __name__ == "__main__":
    print sum_s(10 ** 6)
