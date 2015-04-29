'''
============================================================
Someone has decided to bake a load of cakes and place them on the floor. Our robots can't help but try to find a pattern behind the cakes' disposition. Some cakes form rows, we want to count these rows. A row is a sequence of three or more cakes if we can draw a straight line through its centers. The greater row takes up the smaller rows. So if we have a row with 4 cakes, then we have only one row (not 4 by 3).

The cake locations are represented as a list of coordinates. A coordinate is a list of two integers. You should count the rows.

http://www.checkio.org/mission/cakes-rows/

Created on Apr 5, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
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
        
    def __sub__(self, other):
        return Rational(self.r[0] * other.r[1] - self.r[1] * other.r[0], self.r[1] * other.r[1])

    def __mul__(self, other):
        return Rational(self.r[0] * other.r[0], self.r[1] * other.r[1])

    def __repr__(self): return '%d/%d' % (self.r[0], self.r[1])

def divide_pie(groups):
    remaining, total = Rational(1, 1), sum(group if group > 0 else -group for group in groups)
    for group in groups:
        if group > 0: remaining -= Rational(group, total)
        else: remaining *= Rational(total + group, total)
    return remaining.r

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert isinstance((2, -2), (tuple, list)), "Return tuple or list"
    assert tuple(divide_pie((2, -1, 3))) == (1, 18), "Example"
    assert tuple(divide_pie((1, 2, 3))) == (0, 1), "All know about the pie"
    assert tuple(divide_pie((-1, -1, -1))) == (8, 27), "One by one"
    assert tuple(divide_pie((10,))) == (0, 1), "All together"
