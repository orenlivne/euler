'''
============================================================
http://projecteuler.net/problem=37

The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
============================================================
'''
import itertools

def is_prime(num):
    if num <= 1: return False
    if num == 2 or num == 3: return True
    d = num % 6
    if d != 1 and d != 5: return False
    for i in xrange(6, int(num ** 0.5) + 2, 6):
        if num % (i - 1) == 0 or num % (i + 1) == 0: return False
    return True

def is_prime_restricted(num): # Even-more restricted check, used only to trim x-search space in next function
    d = num % 6
    return d == 1 or d == 5

def sum_truncatable(num):
    '''Return the sum of the first num truncatable primes. Checks numbers < limit.''' 
    s, count = 0, 0
    for x in (x for x in itertools.count(11, 2) if is_prime_restricted(x)):
        x_str = str(x)
        n = len(x_str)
        if (x < 100 or all(int(y) % 2 for y in x_str)) and all(is_prime(int(x_str[i:])) for i in xrange(n)) and all(is_prime(int(x_str[:i])) for i in xrange(1, n)):
            count += 1
            print count, x
            s += x
            if count == num:
                break
    return s
#----------------------------------------------------------------

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
#    print sorted(circular_primes(100))
    import time
    
    start = time.time()
    print sum_truncatable(11)
    print time.time() - start, 'sec'
