'''
============================================================
http://projecteuler.net/problem=117

Using a combination of black square tiles and oblong tiles chosen from: red tiles measuring two units, green tiles measuring three units, and blue tiles measuring four units, it is possible to tile a row measuring five units in length in exactly fifteen different ways.

How many ways can a row measuring fifty units in length be tiled?

NOTE: This is related to problem 116.
============================================================
'''
def F(n):
    '''Works for n >= 4.'''
    f0, f1, f2, f3 = 1, 1, 2, 4
    for _ in xrange(n - 3): f0, f1, f2, f3 = f1, f2, f3, f0 + f1 + f2 + f3
    return f3

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print F(4), F(5), F(50)
