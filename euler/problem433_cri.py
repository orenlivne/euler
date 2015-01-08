#!/usr/bin/env python
'''
============================================================
http://projecteuler.net/problem=433

Let E(x0, y0) be the number of steps it takes to determine the greatest
common divisor of x0 and y0 with Euclid's algorithm. More formally:
x1 = y0, y1 = x0 mod y0
xn = yn-1, yn = xn-1 mod yn-1
E(x0, y0) is the smallest n such that yn = 0.

We have E(1,1) = 1, E(10,6) = 3 and E(6,10) = 4.

Define S(N) as the sum of E(x,y) for 1  x,y  N.
We have S(1) = 1, S(10) = 221 and S(100) = 39826.

Find S(5 x 10^6).
============================================================
'''
import sys
from multiprocessing import Pool, Manager

def writeln(s, lock=None):
    if lock: lock.acquire()
    sys.stdout.write(s + '\n')
    sys.stdout.flush()
    if lock: lock.release()

def gcd_steps(x, y):
    count = 0
    while y: x, y, count = y, x % y, count + 1
    return count

def T(n,N,lock):
    writeln('start %d' % (n, ), lock)
    t = sum(gcd_steps(n, m) for m in xrange(N))
    writeln('t %d' % (n, t), lock)
    return t

def S_partial((n_min, n_max, N, lock)):
    return sum(T(n, N, lock) for n in xrange(n_min, n_max))

if __name__ == "__main__":
    manager = Manager()
    lock = manager.Lock()
    N, n_min, n_max, processes = map(int, sys.argv[1:5])
    step = (n_max - n_min) / processes

    writeln('%s' % repr([(i, min(n_max, i + step)) for i in xrange(n_min, n_max, step)]), lock)

    pool = Pool(processes=processes)
    result = pool.map(S_partial, [(i, min(n_max, i + step), N, lock) for i in xrange(n_min, n_max, step)])
    print sum(result)
