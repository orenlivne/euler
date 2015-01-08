'''
============================================================
http://projecteuler.net/problem=126

The minimum number of cubes to cover every visible face on a cuboid measuring 3 x 2 x 1 is twenty-two.

If we then add a second layer to this solid it would require forty-six cubes to cover every visible face, the third layer would require seventy-eight cubes, and the fourth layer would require one-hundred and eighteen cubes to cover every visible face.

However, the first layer on a cuboid measuring 5 x 1 x 1 also requires twenty-two cubes; similarly the first layer on cuboids measuring 5 x 3 x 1, 7 x 2 x 1, and 11 x 1 x 1 all contain forty-six cubes.

We shall define C(n) to represent the number of cuboids that contain n cubes in one of its layers. So C(22) = 2, C(46) = 4, C(78) = 5, and C(118) = 8.

It turns out that 154 is the least value of n for which C(n) = 10.

Find the least value of n for which C(n) = 1000.
============================================================
'''
import itertools as it
from math import ceil

def C(N):
    print 'N', N
    C = [0] * (N + 1)
    for m in xrange(int(0.5 * (N - 10.) ** 0.5) - 1):
        print '\t', 'm', m
        for a in xrange(1, int(ceil(((N + 2 * m * m - 4 * m) / 6.) ** 0.5)) - m + 1):
            for b in xrange(a, int(ceil(((4 * N + a * a + 8 * (2 - m * a)) ** 0.5 - (4 * m + a)) / 4)) + 1):
                for c in xrange(b, int((N - 4.*m * m - 4 * m * (a + b - 1) - 2 * a * b) / (4 * m + 2 * (a + b))) + 1):
                    n = 4 * m * (m + a + b + c - 1) + 2 * (a * b + a * c + b * c)
                    # print '\t', a, b, c, n
                    if n <= N: C[n] += 1
    # print C
    # print C[22], C[46], C[78], C[118], C[154]
    return C

def n_min(c_val):
    n_max, f = 10 * c_val, lambda (_, c): c != c_val
    while True:
        try: return it.dropwhile(f, enumerate(C(n_max))).next()[0]
        except StopIteration: n_max *= 2 
    
if __name__ == "__main__":
    print n_min(1000)
