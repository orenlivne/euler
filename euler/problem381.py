'''
============================================================
http://projecteuler.net/problem=381

For a prime p let S(p) = (SUM (p-k)!) mod(p) for 1 <= k <= 5.

For example, if p=7,
(7-1)! + (7-2)! + (7-3)! + (7-4)! + (7-5)! = 6! + 5! + 4! + 3! + 2! = 720+120+24+6+2 = 872.
As 872 mod(7) = 4, S(7) = 4.

It can be verified that SUM S(p) = 480 for 5 <= p < 100.

Find SUM S(p) for 5 <= p < 108.
============================================================
'''
from itertools import islice, imap
from problem007 import primes
from problem134 import extended_gcd

inv_mod = lambda x, p: extended_gcd(x, p)[0]
sum_S = lambda N, k: sum(S(p, k) for p in imap(long, primes('lt', N)) if p >= k)
S = lambda p, k: reduce(lambda x, y: (x + y) % p, islice(p_minus_k_factorial_mod(p), k - 2))

def p_minus_k_factorial_mod(p):
    pk, x = p - 2, 1
    while True:
        x *= inv_mod(pk, p)
        yield x
        pk -= 1

if __name__ == "__main__":
    print S(7, 5)  # 4
    print sum_S(10 ** 2, 5)  # 480
    print sum_S(10 ** 8, 5)  # 139602943319822
