'''
============================================================
http://projecteuler.net/problem=114

A row measuring seven units in length has red blocks with a minimum length of three units placed on it, such that any two red blocks (which are allowed to be different lengths) are separated by at least one black square. There are exactly seventeen ways of doing this.

(cf. web page for figure)

How many ways can a row measuring fifty units in length be filled?

NOTE: Although the example above does not lend itself to the possibility, in general it is permitted to mix block sizes. For example, on a row measuring eight units in length you could use red (3), black (1), and red (4).
============================================================
'''
def w(n):
    '''Number of ways for n >= 3.'''
    w0, w1, w2, w3 = 1, 1, 1, 2
    for _ in xrange(n - 3):
        w0, w1, w2, w3 = w1, w2, w3, 2 * w3 - w2 + w0
    return w3
    
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print w(50)
