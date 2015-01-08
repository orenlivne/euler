'''
============================================================
http://projecteuler.net/problem=133

A number consisting entirely of ones is called a repunit. We shall define R(k) to be a repunit of length k; for example, R(6) = 111111.

Let us consider repunits of the form R(10n).

Although R(10), R(100), or R(1000) are not divisible by 17, R(10000) is divisible by 17. Yet there is no value of n for which R(10n) will divide by 19. In fact, it is remarkable that 11, 17, 41, and 73 are the only four primes below one-hundred that can be a factor of R(10n).

Find the sum of all the primes below one-hundred thousand that will never be a factor of R(10n).
============================================================
'''
from itertools import ifilter, islice
from problem012 import factorize
from problem129 import A
from problem007 import primes

ten_factors = [2, 5]

def other_factor(k, factors):
    '''Does k have other primes factors than the list ''factors''?'''
    i, l = 0, len(factors)
    while i < l and k > 1:
        if k % factors[i] == 0: k /= factors[i]
        else: i += 1
    return k > 1

def sum_using_other_factor(max_prime):
    s = 0
    for p in islice(primes('lt', max_prime), 3, 100000000):
        a = A(p)
        other_fac = other_factor(a, ten_factors)
        if other_fac:
            s += p 
        print p, a, other_fac, s
    return s + 10  # 10=2+3+5 = boundary case

def sum_using_max_n(max_prime, n=16):
    k = 10 ** n
    return sum(p for p in primes('lt', max_prime) if pow(10, k, int(9 * p)) != 1)

sum_mine = lambda max_prime: 10 + sum(p for (p, _) in ifilter(lambda (_, a): not (factorize(a).keys() <= ten_factors), ((p, A(p)) for p in primes('lt', max_prime) if p != 2 and p != 5)))
    
if __name__ == "__main__":
    N = 10 ** 5
    print sum_using_max_n(N)
    print sum_using_other_factor(N)
    print sum_mine(N)
