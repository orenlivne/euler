'''
============================================================
http://projecteuler.net/problem=35

The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
============================================================
'''
from problem007 import primes

def circular_primes(n):
    '''Returns the set of circule primes < n.'''
    p = filter(is_odd, primes('lt', n)) # Odd-digit prime list
    c = set([2])
    for x in p:
        examine_prime(x, p, c)
    return c

def is_odd(x):
    '''Is x made of odd digits only?'''
    while x > 0:
        if (x % 10) % 2 == 0:
            return False
        x /= 10
    return True

def examine_prime(x, p, c):
    '''Add a prime x and its cyclic permutations to c if it is a circular prime. p = prime list.
    Note: prime list (all primes < n) must include all perms of x. This automatically happens if n
    is a power of 10, since all perms all have the same # digits as x.'''
    if x in c:      # x already circular, nothing to do
        return
    k, y = num_digits(x) - 1, x
    shift = 10 ** k
    for _ in xrange(k):     # Loop over #digits-1 perms of x, since we already know x in prime.
        d = y % 10
        if d % 2 == 0:      # Encountered even digit ==> there existsa non-prime perm when this digit becomes the right-most one
            return
        y = d * shift + (y / 10) # Cyclic perm
        if not y in p:           # Perm is not prime
            return
        
    # x is cyclic, add it and its perms to c
    y = x
    c.add(y)
    for _ in xrange(k):
        y = (y % 10) * shift + (y / 10)
        c.add(y)

def num_digits(x):
    '''Return the number of decimal digits of x. x >= 1.'''
    count = 0
    while x > 0:
        x /= 10
        count += 1
    return count

#----------------------------------------------------------------
# RB14's solution (from Israel) 17 Feb 2013 05:21 pm.
# Slightly faster than mine.

def is_prime(num): # Restricted check, assumes num >= 4
    #if num % 2 == 0 or num % 3 == 0: return False
    d = num % 6
    if d != 1 and d != 5: return False
    for i in xrange(6, int(num ** 0.5) + 2, 6):
        if num % (i - 1) == 0 or num % (i + 1) == 0: return False
    return True

def is_prime_restricted(num): # Even-more restricted check, used only to trim x-search space in next function
    #if num % 2 == 0 or num % 3 == 0: return False
    d = num % 6
    return d == 1 or d == 5

def problem35_RB14():
    circ_primes = [2, 3]
    for x in (x for x in xrange(5, 1000000, 2) if is_prime_restricted(x)):
        x_str = str(x)
        # Checks first that x includes only odd digits
        if all(int(y) % 2 for y in x_str) and all(is_prime(y) for y in (int(x_str[i:] + x_str[0:i]) for i in xrange(len(x_str)))):
            circ_primes.append(x)
    return len(circ_primes)
#----------------------------------------------------------------

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
#    print sorted(circular_primes(100))
    import time
    
    start = time.time()
    print len(circular_primes(1000000))
    print time.time() - start, 'sec'
    
    start = time.time()
    print problem35_RB14()
    print time.time() - start, 'sec'
