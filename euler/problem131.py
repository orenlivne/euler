'''
============================================================
http://projecteuler.net/problem=131

There are some prime values, p, for which there exists a positive integer, n, such that the expression n3 + n2p is a perfect cube.

For example, when p = 19, 83 + 8219 = 123.

What is perhaps most surprising is that for each prime with this property the value of n is unique, and there are only four such primes below one-hundred.

How many primes below one million have this remarkable property?
============================================================
'''
from problem035 import is_prime

pnum = lambda N: sum(1 for a in xrange(1, int((-3 + (12 * N - 3) ** 0.5) / 6.) + 1) if is_prime(3 * a * (a + 1) + 1)) 

if __name__ == "__main__":
    print pnum(10 ** 6)
