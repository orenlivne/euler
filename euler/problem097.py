'''
============================================================
http://projecteuler.net/problem=97

The first known prime found to exceed one million digits was discovered in 1999, and is a Mersenne prime of the form 269725931; it contains exactly 2,098,960 digits. Subsequently other Mersenne primes, of the form 2p1, have been found which contain more digits.

However, in 2004 there was found a massive non-Mersenne prime which contains 2,357,207 digits: 2843327830457+1.

Find the last ten digits of this prime number.
============================================================
'''
def two_n_mod(n, p):
    '''Returns 2**n mod p, n >= 1.'''
    x, y = 1, 2
    while n:
        n, b = divmod(n, 2)
        if b: x = (x * y) % p
        y = (y * y) % p
    return x

if __name__ == "__main__":
    d = 10
    p = 10 ** d
    print ('%%0%dd' % (d,)) % ((28433 * two_n_mod(7830457, p) + 1) % p,)
