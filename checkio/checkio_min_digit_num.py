'''
============================================================
http://min_digit_num.org

You are given a two or more digits number n. For this
mission, you should find the smallest positive number m such
that the product of its digits equals n. If m does not
exist, then return 0.

Example: n = 20 = 2*10 but 10 is not a digit. Also, we can
factorize n = 2*2*5, smallest is 225. For 4*5 -- 45. So
m = 45.

Hints: remember prime numbers and be careful with endless
loops. 

Precondition: 9 < n < 10**5.
============================================================
'''
import itertools
from numpy.ma.testutils import assert_equal

def primes(n):
    '''Return the list of primes <= n using the Sieve of Erasthosenes'.
    http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes'''
    s = [False] * 2 + [True] * (n - 1)
    for p in xrange(2, int(n ** 0.5) + 1):
        for x in xrange(p * p, n + 1, p): s[x] = False
    return [x for x in xrange(n) if s[x]]

class DigitFactorizer(object):
    '''A helper class that factorizes numbers up to a limit max_n, distinguishing between
     factors < 10 and >= 10.'''
    def __init__(self, max_n):
        self._max_n = max_n
        self._max_factor = 10
        self._primes = primes(max_n)
        # Number of "relevant" primes < max_factor = size of powers arrays to allocate
        # in factorize_to_digits()
        self._alloc_size = itertools.dropwhile(lambda (i, x): x < self._max_factor,
                                               enumerate(self._primes)).next()[0]
    
    def factorize_to_digits(self, n):
        '''Factorize n >= 2 into primes using the prime list ''primes''. Return
        None if n has a factor >= max_factor. Otherwise, return an array with the number
        of prime powers < max_factor that n is divisible by.'''
        powers, i = [0] * self._alloc_size, 0
        for i, p in enumerate(self._primes):
            if p >= self._max_factor: return None
            count = 0
            while n != 1 and n % p == 0:
                count += 1
                n /= p
            powers[i] = count
            if n == 1: return powers

    def min_prod_num(self, n):
        '''Return the minimum number m whose digit product equals n. n >= 2.'''
        powers = self.factorize_to_digits(n)
        
        # If there exists a factor > 10, no solution 
        if not powers: return 0
        
        # All 5's and 7's cannot be multiplied by any other factor to obtain m's digits,
        # since it would make them > 10 and not a digit. So remove them from n. Note that in
        # the smallest m the digits are sorted in increasing order from left to right, so
        # keep this order in the loops below (5's all first, then all 7's).    
        s = '' # Holds the textual representation of m. Easier to work with than an int.
        for i, p in ((2, 5), (3, 7)):
            p_str = repr(p)
            for _ in xrange(powers[i]):
                n /= p
                s += p_str
        
        # We're reduced the problem to n = 2^a * 3^b. First, remove powers of 9 (they have to go
        # together - this scheme can only make m smaller compared with other pairings of two 3's). 
        i, p = 1, 9
        p_str = repr(p)
        while n % p == 0:
            n /= p
            s += p_str

        if n % 3 != 0:
            # Case 1: n = 2^a. Group 2's into triplets (=powers of 8). Whatever's left is
            # the remaining m-digit.
            i, p = 0, 8
            p_str = repr(p)
            while n % p == 0:
                n /= p
                s += p_str
            if n > 1: s += repr(n) # If there's a remaining digit, add it to m
            s = ''.join(sorted(s))  # The smallest m is composed of increasing digits 
        else:
            # Case 2: n = 2^a * 3. Compare the two options "lone 3" and "(2,3)" and and
            # pick the better one. The second option exists only if a > 0.
            i, p = 0, 8
            p_str = repr(p)
            
            temp, t1 = n / 3, '3'
            while temp % p == 0:
                # Option 1
                temp /= p
                t1 += p_str
            if temp > 1: t1 += repr(temp) # If there's a remaining digit, add it to m
            t1 = ''.join(sorted(s + t1))
            
            if n % 6 == 0:
                # Option 2
                temp, t2 = n / 6, '6'
                while temp % p == 0:
                    temp /= p
                    t2 += p_str
                if temp > 1: t2 += repr(temp) # If there's a remaining digit, add it to m
                t2 = ''.join(sorted(s + t2))
                s = min(t1, t2)
            else:
                s = t1 
        
        return int(s)

#---------------------------------------------
# Testing
#---------------------------------------------
'''A global object that caches the prime list so that each min_digit_num() call does not incur this overhead.'''
DIGIT_FACTORIZER = DigitFactorizer(10 ** 5)

def min_digit_num(n):
    '''Main call. Calculates m given n.''' 
    return DIGIT_FACTORIZER.min_prod_num(n)
    
if __name__ == "__main__":
    assert_equal(min_digit_num(20), 45, '1st example: n = 20') 
    assert_equal(min_digit_num(21), 37, '2nd example: n = 21') 
    assert_equal(min_digit_num(17), 0, '3rd example: n = 17') 
    assert_equal(min_digit_num(33), 0, '4th example') 
    assert_equal(min_digit_num(3125), 55555, '5th example') 
    assert_equal(min_digit_num(9973), 0, '6th example') 
 
    assert_equal(min_digit_num(24), 38, '7th example: n = 24') # A test case of Case 1
    assert_equal(min_digit_num(36), 49, '7th example: n = 36')
