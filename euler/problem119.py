'''
============================================================
http://projecteuler.net/problem=119

The number 512 is interesting because it is equal to the sum of its digits raised to some power: 5 + 1 + 2 = 8, and 83 = 512. Another example of a number with this property is 614656 = 284.

We shall define an to be the nth term of this sequence and insist that a number must contain at least two digits to have a sum.

You are given that a2 = 512 and a10 = 614656.

Find a30.
============================================================
'''
from itertools import islice, count
from math import ceil, log10

digit_sum = lambda x: sum(map(int, str(x)))

def digit_sum_pow():
    '''Returns an iterator of {an}_{n>=1}.'''
    log9 = log10(9)
    for m in count(2):
        logm, A = log10(m), []
        for k in xrange(int(ceil((m - 1) / (log9 + logm))), int(ceil(m / logm))):
            for S in xrange(int(ceil(10 ** ((m - 1.) / k))), int(ceil(10 ** ((1.0 * m) / k)))):
                a = S ** k
                if digit_sum(a) == S: A.append(a)
        for a in sorted(A): yield a
        
if __name__ == "__main__":
    print islice(digit_sum_pow(), 29, 30).next()
