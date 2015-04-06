'''
============================================================
Someone has decided to bake a load of cakes and place them on the floor. Our robots can't help but try to find a pattern behind the cakes' disposition. Some cakes form rows, we want to count these rows. A row is a sequence of three or more cakes if we can draw a straight line through its centers. The greater row takes up the smaller rows. So if we have a row with 4 cakes, then we have only one row (not 4 by 3).

The cake locations are represented as a list of coordinates. A coordinate is a list of two integers. You should count the rows.

http://www.checkio.org/mission/cakes-rows/

Created on Apr 5, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from collections import Counter

def gcd(m, n):
    '''Returns the greatest common divisor of m and n. Eulid''s algorithm.'''
    while n: m, n = n, m % n
    return m
    
class Rational(object):
    '''Rational number m/n.'''
    def __init__(self, m, n=1):
        # Standardize the rational representation: enforce n > 0 and gcd(m,n)=1.
        if n < 0: m, n = -m, -n
        if m == 0: n = 1
        g = gcd(m, n)
        self.r = (m / g, n / g)

    # So that we can use Rationals as dictionary keys. 
    def __key(self): return self.r
    def __hash__(self): return hash(self.__key())
    def __eq__(self, other): return self.r == other.r
    def __repr__(self): return '%d/%d' % (self.r[0], self.r[1])

def make_line((x1, y1), (x2, y2)):
    '''Returns a tuple of line parameters of the unique line passing through two integer points.
    Vertical line, 1*x + 0*y = x1
    Normal line: y - y1 = m*(x - x1), i.e., -m*x + y = y1 - m*x1.'''
    return (Rational(1), Rational(0), Rational(x1)) if x1 == x2 else \
    (Rational(y1 - y2, x2 - x1), Rational(1), Rational((x2 - x1) * y1 - x1 * (y2 - y1), x2 - x1))

def number_of_lines(points):
    '''Returns the number of lines passing through at least 3 points in a list of integer points.'''
    points = map(tuple, points)
    return sum(1 for _, v in Counter((make_line(a, b), 1) for a in points for b in points if a < b).iteritems() if v >= 2)

if __name__ == "__main__":
    assert number_of_lines([[3, 3], [5, 5], [8, 8], [2, 8], [8, 2]]) == 2
    assert number_of_lines([[2, 2], [2, 5], [2, 8], [5, 2], [7, 2], [8, 2], [9, 2], [4, 5], [4, 8], [7, 5], [5, 8], [9, 8]]) == 6
