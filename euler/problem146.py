'''
============================================================
http://projecteuler.net/problem=146

The smallest positive integer n for which the numbers n2+1, n2+3, n2+7, n2+9, n2+13, and n2+27 are consecutive primes is 10. The sum of all such integers n below one-million is 1242490.

What is the sum of all such integers n below 150 million?
============================================================
'''
from problem007 import primes
from problem027 import is_prime
from random import choice

'''Fermat probable primality test'''
N_LIST = 10 ** 6
SQRT_N_LIST = int(N_LIST ** 0.5)
P = primes('lt', SQRT_N_LIST + 1)
is_probable_prime = lambda n, tries = 20: all(pow(int(choice(P)), n - 1, n) == 1 for _ in xrange(tries)) 
isp = lambda x, tries = 20: is_prime(x, P) if x <= N_LIST else is_probable_prime(x, tries=tries)

def consecutive_n(N, offset, complement, mods_primes=50):
    '''Return n for which {n^2+x: x in offset} is prime and {n^2+x: x in complement} is not prime.''' 
    # Tabulate permissible remainders n mod p for the first mods_primes primes p
    p_list = primes('first', mods_primes)
    nc = int(p_list[-1] ** 0.5) + 1
    R = [[all((i2 + x) % p for x in offsets) for i2 in (i * i for i in xrange(p))] for p in p_list]
    # By the Chinese remainder theorem, n must be of the form 210q + [10|80|130|200]
    for s in [10, 80, 130, 200]:
        for n in xrange(s, N, 210):
            n2 = n * n
            # First check against remainder table; if passes, run the more expensive primality test
            if (n <= nc or all(R[i][n % p] for i, p in enumerate(p_list))) and \
            all(isp(n2 + x) for x in offsets) and all(not isp(n2 + x) for x in complement):
                yield n
             
if __name__ == "__main__":
    offsets = [1, 3, 7, 9, 13, 27]
    complement = [21]  # No need to check other offsets in the range [2,26] since they are composite for n=210q + [10|80|130|200] 
    print sum(consecutive_n(10 ** 6, offsets, complement))  # 1242490
    print sum(consecutive_n(int(1.5 * 10 ** 8), offsets, complement))  # 676333270
