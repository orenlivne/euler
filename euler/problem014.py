'''
============================================================
http://projecteuler.net/problem=14

n  n/2 (n is even)
n  3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13  40  20  10  5  16  8  4  2  1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, time

def collatz(x):
    '''Collatz chain starting at x.'''
    yield x
    while x != 1:
        x = x / 2 if x % 2 == 0 else 3 * x + 1
        yield x

def collatz_max(n):
    '''starting number, under n, producing the longest Collatz chain.

    >>> collatz_max(1000000)
    104743
    '''
    s = np.zeros((n,), dtype=np.uint)
    for x in xrange(n - 1, 0, -1): # Largest #'s produce longest paths => faster sieving. So we loop in reverse
        if s[x] == 0:
            chain = np.array(list(collatz(x)))
            i = np.arange(len(chain), 0, -1, dtype=np.uint)
            j = np.where(chain < n)[0]
            k = j[np.where(s[chain[j]] == 0)]
            s[chain[k]] = i[k] 
    return np.argmax(s)  

def collatz_max_nostorage(n):
    '''Brute-force, no storage'''
    lm, xm = 0, 0
    for x in xrange(1, n):
        l = sum(1 for _ in collatz(x))
        if l > lm:
            lm = l
            xm = x  
    return xm

if __name__ == "__main__":
    start = time.time()
    x = collatz_max_nostorage(1000000)
    print x, time.time() - start, 'sec'

    start = time.time()
    x = collatz_max(1000000)
    print x, time.time() - start, 'sec'
    
    #import doctest
    #doctest.testmod()
