'''
============================================================
http://projecteuler.net/problem=57

It is possible to show that the square root of two can be expressed as an infinite continued fraction.

 2 = 1 + 1/(2 + 1/(2 + 1/(2 + ... ))) = 1.414213...

By expanding this for the first four iterations, we get:

1 + 1/2 = 3/2 = 1.5
1 + 1/(2 + 1/2) = 7/5 = 1.4
1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The next three expansions are 99/70, 239/169, and 577/408, but the eighth expansion, 1393/985, is the first example where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than denominator?
============================================================
'''
import itertools as it

def expansion():
    p, q = 1, 1
    while True:
        s = p + q
        p, q = s + q, s
        yield p, q

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print sum(1 for p, q in it.islice(expansion(), 1000) if len(str(p)) > len(str(q)))

    for k, (p, q) in enumerate(it.islice(expansion(), 100)):
        print k, (p, q)

    import numpy as np
    a = np.array([(k + 1) for k, (p, q) in enumerate(it.islice(expansion(), 400)) if len(str(p)) > len(str(q))])
    print a
    print np.diff(a)
