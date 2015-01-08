'''
============================================================
http://projecteuler.net/problem=85

By counting carefully it can be seen that a rectangular grid measuring 3 by 2 contains eighteen rectangles:
Although there exists no rectangular grid that contains exactly two million rectangles, find the area of the grid with the nearest solution.
============================================================
'''
'''Return the index of x in the triangular number series. If non-integer, x is not triangular.''' 
tri_num = lambda x: 0.5 * (-1 + (1 + 8 * x) ** 0.5)

'''Return the list of triangular numbers between 1 and x, inclusive.'''
tris_le = lambda x: [(n * (n + 1)) / 2 for n in xrange(1, int(tri_num(x)) + 1)]

def tri_check(x):
    '''Check if x is a triangular number. If so, return the triangular index of x, otherwise -1.'''
    n = tri_num(x)
    return int(n) if (n < int(n) + 1e-10) else -1

def closest_area(a):
    T = tris_le(a ** 0.5)
    for y in (a + s * i for i in xrange(a) for s in [-1, 1]):
        #print 'y', y
        for n, tn in enumerate(T, 1):
            if y % tn == 0:
                m = tri_check(y / tn)
                #print '\t', 'n', n, 'tn', tn, 'y/tn', y / tn, 'm', m 
                if m > 0:
                    return m * n
            
if __name__ == "__main__":
    print closest_area(2000000)
