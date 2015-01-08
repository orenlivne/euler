'''
============================================================
http://projecteuler.net/problem=39

If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, 
there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p  1000, is the number of solutions maximised?
============================================================
'''
import numpy as np

def num_triplets(d):
    '''Returns an array with #integer Pythagorean triplets (a,b,c) for each 0 <= p=a+b+c <= d.'''
    n = np.zeros((d + 1,), dtype=np.uint)
    for a in xrange(1, int(d / (2 + 2 ** .5)) + 1):
        for b in xrange(a, int(d * (d - 2) / (2.*(d - 1)) + 1)):
            cr = (a * a + b * b) ** .5
            c = int(cr)
            if cr - c < 1e-15:  # Integer solution (a,b,c)
                p = a + b + c
                if p <= d: n[p] += 1
    return n

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    # np.set_printoptions(threshold=np.nan)
    # n = num_triplets(1000)
    # print n[120]
    a = num_triplets(1000)
    print np.where(a), a[np.where(a)]
    #print np.argmax(num_triplets(1000))
