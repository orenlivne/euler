'''
============================================================
http://projecteuler.net/problem=225

The sequence 1, 1, 1, 3, 5, 9, 17, 31, 57, 105, 193, 355, 653, 1201 ...
is defined by T1 = T2 = T3 = 1 and Tn = Tn-1 + Tn-2 + Tn-3.

It can be shown that 27 does not divide any terms of this sequence.
In fact, 27 is the first odd number with this property.

Find the 124th odd number that does not divide any terms of the above sequence.
============================================================
'''
from itertools import islice, count

def divides_tri(k):
    a, b, c = 1, 1, 1
    while True:
        a, b, c = b, c, (a + b + c) % k
        if a == 0 or b == 0 or c == 0: return True
        if a == 1 and b == 1 and c == 1: return False

def odd_not_dividing_tri():
    for x in (2 * y + 1 for y in count(1)):
        if not divides_tri(x): yield x

if __name__ == "__main__":
    print islice(odd_not_dividing_tri(), 0, 1).next()
    print islice(odd_not_dividing_tri(), 123, 124).next()
    
