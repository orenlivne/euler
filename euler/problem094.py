'''
============================================================
http://projecteuler.net/problem=94

It is easily proved that no equilateral triangle exists with integral length sides and integral area. However, the almost equilateral triangle 5-5-6 has an area of 12 square units.

We shall define an almost equilateral triangle to be a triangle for which two sides are equal and the third differs by no more than one unit.

Find the sum of the perimeters of all almost equilateral triangles with integral side lengths and area and whose perimeters do not exceed one billion (1,000,000,000).
============================================================
'''
from problem066 import pell_solution
from itertools import takewhile, ifilter

def pell_solutions(D, s=1):
    '''An iterator of all solutions to Pell''s equation x**2-D*y**2=s. s must be 1 or -1.
    Note: s=-1 only has solutions if the period of the continued fraction of D**0.5 is odd.
    Otherwise, this method will block.'''
    x1, y1 = pell_solution(D, s)
    yield x1, y1
    x, y, t = x1, y1, 1
    while True:
        x, y, t = x1 * x + D * y1 * y, x1 * y + y1 * x, -t
        if s > 0 or t > 0: yield x, y
    
def sum_aet_case(N, s):
    '''Returns the sum of Almost Equilateral Triangles (AET) perimeters for case A - a,a,a+1 sides
    (s=-1) or case B - a,a,a-1 sides (s=1).'''
    x_max, x_mod = 0.5 * N + s, 2 if s > 0 else 1
    return 2 * sum(x - s for x, _ in takewhile(lambda (x, y): x < x_max, ifilter(lambda (x, y): x > 2 and ((2 * x - s) % 3 == 0) and (x % 3 == x_mod or y % 3 == 0), pell_solutions(3))))

sum_aet = lambda N: sum_aet_case(N, -1) + sum_aet_case(N, 1)

#---------------- http://www.mathblog.dk/project-euler-94-almost-equilateral-triangles/ ------
def cross_check(N, s):
    x, y = 2, 1
    while True:
        if (x > 0.5 * N + s): return
        if ((2 * x - s) % 3 == 0) and (y % 3 == 0 or (x - 2 * s) % 3 == 0):
            yield x, y
        x, y = 2 * x + y * 3, y * 2 + x
        
if __name__ == "__main__":
#     N = 10 ** 9
#     for s in [-1, 1]:
#         print 's', s
#         x_max, x_mod = 0.5 * N + s, 2 if s > 0 else 1
#         print list(takewhile(lambda (x, y): x < x_max, pell_solutions(3)))
#         print list(takewhile(lambda (x, y): x < x_max, ifilter(lambda (x, y): ((2 * x - s) % 3 == 0) and (x % 3 == x_mod or y % 3 == 0), pell_solutions(3))))
#         print list(2 * (x - s) for x, _ in takewhile(lambda (x, y): x < x_max, ifilter(lambda (x, y): ((2 * x - s) % 3 == 0) and (x % 3 == x_mod or y % 3 == 0), pell_solutions(3))))
#         print 2 * sum(x - s for x, _ in takewhile(lambda (x, y): x < x_max, ifilter(lambda (x, y): ((2 * x - s) % 3 == 0) and (x % 3 == x_mod or y % 3 == 0), pell_solutions(3))))
    print sum_aet(10 ** 9)
    print list(cross_check(10 ** 9, -1))
    print list(cross_check(10 ** 9, 1))
