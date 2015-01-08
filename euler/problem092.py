'''
============================================================
http://projecteuler.net/problem=92

A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.

For example,

44  32  13  10  1  1
85  89  145  42  20  4  16  37  58  89

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?
============================================================
'''
import numpy as np
cycles = [(0,), (1,), (89, 145, 42, 20, 4, 16, 37, 58)]
seq = lambda x: sum(x * x for x in map(int, str(x)))

#------------------------------- Oren - brute-force with memoization ---------------------------- 
def cycle_index(seq, cycles, n, queue_size=300):
    '''Returns an array with the asymptotic cycle number of all starting numbers 0 <= x < n.'''
    c, q, x = np.zeros((n,), dtype=np.short), np.zeros((queue_size,), dtype=np.uint), 0
    for k, cycle in enumerate(cycles, 1): c[np.array(cycle)] = k  # Initial conditions
    while x < n:
        last, y = 0, x  # last = (current size of the queue q) - 1
        q[last] = y
        while not c[y]:  # While y is not yet assigned to a cycle, advance the path
            last += 1
            y = seq(y)
            q[last] = y
        # print last, q[:last + 1], c[y]
        c[q[:last + 1]] = c[y]  # Assign all numbers in the queue to the same cycle index since they're on the same path
        while x < n and c[x]: x += 1  # Advance pointer to next non-assigned number
    return c
    
#-------------------- From thread --------------------------------
from numpy import around
from scipy.special import binom
from itertools import combinations_with_replacement, islice, imap, groupby

def multinom(n, K):
    '''Multinomial coefficient of choosing K[0],...,K[-1] from n objects.'''
    fac, tot = 1, n
    for k in K:
        fac *= int(around(binom(tot, k)))
        tot -= k
    return fac

def ends_at(seq, x, end_x, alt_x):
    '''If x''s sequence ends with end_x, return True; if it ends with alt_x, return False. Must contain
    either one.'''
    while True:
        if x == end_x: return True
        if x == alt_x : return False
        x = seq(x)
        
digit_counts = lambda x: [sum(1 for _ in g) for _, g in groupby(x)]
num_ending_at = lambda seq, end_x, alt_x, num_digits: sum(multinom(num_digits, occur) for occur in (digit_counts(str(x)) for x in (int(''.join(x)) for x in islice(combinations_with_replacement(imap(str, xrange(10)), num_digits), 1, None)) if ends_at(seq, x, end_x, alt_x)))

if __name__ == "__main__":
    # Fast solution
    print num_ending_at(seq, 89, 1, 7)
    
    # Brute-force
    c = cycle_index(seq, cycles, 10000000)
    print len(np.where(c == c[89])[0])
