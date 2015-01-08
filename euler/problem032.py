'''
============================================================
http://projecteuler.net/problem=32

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39  186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
============================================================
'''
import itertools

DIGITS = range(1, 10)
MOD9 = dict([(0, 0), (1, 4), (3, 6), (4, 1), (6, 3), (7, 7)])
SINGLE_DIGITS = [3, 4, 6, 7, 9] # 1-digit a-options
SINGLE_DIGITS_A2 = [1] + SINGLE_DIGITS # a mod 9 options for 2-digit a's

def is_pandigital((a, b)):
    '''Is the triplet (a,b,a*b) 9-pandigitial?'''
    return sorted(digits(a) + digits(b) + digits(a * b)) == DIGITS

digits = lambda a: map(int, str(a))

def to_decimal(digits):
    '''Convert a digit list to a decimal number using Horner's rule.'''
    x = digits[0]
    for i in xrange(1, len(digits)):
        x = 10 * x + digits[i]
    return x

def b4(a):
    '''4-digit b-options given a 1-digit a.'''
    bm = MOD9[a % 9]
    for b0 in (x for x in DIGITS if x != a):
        for b1 in (x for x in DIGITS  if x != a and x != b0):
            for b2 in (x for x in DIGITS  if x != a and x != b0 and x != b1):
                b3 = (bm - b0 - b1 - b2) % 9
                if b3 == 0:
                    b3 = 9
                yield to_decimal([b0, b1, b2, b3])

a2 = lambda: itertools.ifilter(lambda x: x % 10 != 0, (a for am in SINGLE_DIGITS_A2 for a in xrange(am + 9, 73 + am, 9))) # 2-digit a-options

def b3(a):
    '''3-digit b-options given a 2-digit a.'''
    bm = MOD9[a % 9]
    for b0 in (x for x in DIGITS if x != a):
        for b1 in (x for x in DIGITS  if x != a and x != b0):
            b2 = (bm - b0 - b1) % 9
            if b2 == 0:
                b2 = 9
            yield to_decimal([b0, b1, b2]) 
            
options14 = lambda : ((a, b) for a in SINGLE_DIGITS for b in b4(a)) # 1-digit x 4-digit candidate pandigital pairs
options23 = lambda : ((a, b) for a in a2() for b in b3(a)) # 2-digit x 3-digit candidate pandigital pairs
pan_sum = sum(set(list(map(lambda (a, b): a * b, filter(is_pandigital, itertools.chain(options14(), options23())))))) 

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    import time
    
    print pan_sum
    n = 10000
    start = time.time()
    for _ in xrange(n):
        a = pan_sum
    print (time.time() - start) / n, 'sec'

    start = time.time()
    print sum(set(list(map(lambda (a, b): a * b, filter(is_pandigital,
                                                        itertools.chain(
                                                        ((a, b) for a in xrange(1, 10) for b in xrange(1234, 9877)),
                                                        ((a, b) for a in xrange(11, 99) for b in xrange(100, 988)),
                                                        ))))))
    print time.time() - start, 'sec'
