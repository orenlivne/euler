'''
============================================================
http://www.checkio.org/mission/counting-tiles/solve/

Created on Apr 26, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import math

def circle_height(x, radius):
    return (radius * radius - x * x) ** 0.5

def checkio(radius):
    """count tiles. O(radius) solution. Could be improved with Gauss' asymptotics """
    r, q = divmod(radius, 1)
    r = int(r)
#     print r, q
#     print 'heights', [circle_height(i, radius) for i in xrange(r + 1)]
#     print 'full', [int(circle_height(i + 1, radius)) for i in xrange(r)]
#     print 'partial', [int(math.ceil(circle_height(i, radius)) - int(circle_height(i + 1, radius))) for i in xrange(r)]
    whole, partial = sum(int(circle_height(i + 1, radius)) for i in xrange(r)), \
    sum(int(math.ceil(circle_height(i, radius)) - int(circle_height(i + 1, radius))) for i in xrange(r))
    if q > 0:
#        print 'last', circle_height(r, radius)
        partial += int(math.ceil(circle_height(r, radius)))
#    print 4 * whole, 4 * partial
    return [4 * whole, 4 * partial]

# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(2.5) == [12, 20], "N=2.5"
    assert checkio(2.1) == [4, 20], "N=2.1"
    assert checkio(2) == [4, 12], "N=2"
    assert checkio(3) == [16, 20], "N=3"
