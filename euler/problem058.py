'''
============================================================
http://projecteuler.net/problem=58

Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more interesting is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of 8/13  62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9 will be formed. If this process is continued, what is the side length of the square spiral for which the ratio of primes along both diagonals first falls below 10%?
============================================================
'''
from itertools import dropwhile
import numpy as np

#------------------------------
# Common routines
#------------------------------
def is_prime(num):
    if num <= 1: return False
    if num == 2 or num == 3: return True
    d = num % 6
    if d != 1 and d != 5: return False
    for i in xrange(6, int(num ** 0.5) + 2, 6):
        if num % (i - 1) == 0 or num % (i + 1) == 0: return False
    return True

class PrimeFractionIterator(object):
    '''An iterator that outputs the prime ratio for n=1,2,... where k=2*k+1 is the spiral side length.'''
    def __init__(self):
        self.count = 1
        self.count_prime = 0
        self.n = 0
        self.d = 1
    
    def __iter__(self):
        return self

    def next(self):
        '''Output ratio for n=1,2,... where k=2*k+1 is the spiral side length.'''
        self.n += 1
        n2 = 2 * self.n
        self.count += 4
        for _ in xrange(3):  # Check only a,b,c
            self.d += n2
            self.count_prime += is_prime(self.d)
        self.d += n2
        return self.n, (1.0 * self.count_prime) / self.count

#------------------------------
# Brute-force solution
#------------------------------
def smallest_side_brute_force(r):
    '''Return the smallest k=2*n+1 for which the prime ratio r(k) < r.'''
    return 2 * dropwhile(lambda x: x[1] >= r, PrimeFractionIterator()).next()[0] + 1

#------------------------------
# Model fitting & extrapolation
#------------------------------
def inverse_extrapolation(s):
    '''Estimate the value of n by Newton's iteration on log(n)/n - s = 0. Since n rounded to
    an integer, an adequate stopping criterion is that the difference between iterates < 0.5.'''
    n = 1.0 / s
    logn = np.log(n)
    n_next = n * (1 - (logn - s * n) / (1 - logn))
    while abs(n_next - n) >= 0.5:
        n = n_next
        logn = np.log(n)
        print n
        n_next = n * (1 - (logn - s * n) / (1 - logn))
    return np.ceil(n)

def fit_and_estimate(k_fit, r):
    p = PrimeFractionIterator()
    for _ in xrange(25): p.next()
    data = zip(*[p.next() for _ in xrange(k_fit)])
    n_data, r_data = np.array(data[0]), np.array(data[1])
    scaled_data = 1.0 / n_data
    print r_data / scaled_data
    a = np.polyfit(scaled_data[0:100], r_data[0:100], 4)
    r_model = np.polyval(a, scaled_data)
    e = np.sqrt(sum((r_data - r_model) ** 2) / k_fit)
    print len(r_data), a, e
    return 0.0, n_data, scaled_data, r_data, r_model, a

if __name__ == "__main__":
    result, n, s, r, r_model, a = fit_and_estimate(400, 0.1)
    
#     import time
#     r = 0.4
#     for i in xrange(3):    
#         num_calls = 20 if r > 0.1 else 1
#         t = time.time()
#         for _ in xrange(num_calls):
#             k = smallest_side_brute_force(r)
#         t = (time.time() - t) / num_calls
#         print '%.2e %6d %.3e' % (r, k, t) 
#         r *= 0.5
#     
