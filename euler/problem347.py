'''
============================================================
http://projecteuler.net/problem=347

The largest integer <= 100 that is only divisible by both the primes 2 and 3 is 96, as 96=32*3=25*3. For two distinct primes p and q let M(p,q,N) be the largest positive integer <=N only divisible by both p and q and M(p,q,N)=0 if such a positive integer does not exist.

E.g. M(2,3,100)=96.
M(3,5,100)=75 and not 90 because 90 is divisible by 2 ,3 and 5.
Also M(2,73,100)=0 because there does not exist a positive integer <= 100 that is divisible by both 2 and 73.

Let S(N) be the sum of all distinct M(p,q,N). S(100)=2262.

Find S(10,000,000).
============================================================
'''
from itertools import takewhile
from math import ceil, log
from problem007 import primes

def sum_distinct_m(N):
    '''Return the sum of distinct M(p,q,N) for all p<q prime pairs.''' 
    P, p_max = map(long, primes('lt', int(ceil(N * 0.5)) + 1)), N ** 0.5
    return sum(max(p ** k * q ** l
                   for k in xrange(1, int(log(float(N) / q) / log(p)) + 1) 
                   for l in xrange(1, int(log(float(N) / p ** k) / log(q)) + 1))
               for (p, q) in
               ((p, q) for (i, p) in takewhile(lambda p: p[1] <= p_max, enumerate(P))
                for q in (P[j] for j in takewhile(lambda j: P[j] <= N / P[i], xrange(i + 1, len(P))))))

if __name__ == "__main__":
    print sum_distinct_m(10 ** 7)
