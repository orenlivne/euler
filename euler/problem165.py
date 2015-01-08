'''
============================================================
http://projecteuler.net/problem=165

A segment is uniquely defined by its two endpoints.
By considering two line segments in plane geometry there are three possibilities:
the segments have zero points, one point, or infinitely many points in common.

Moreover when two segments have exactly one point in common it might be the case that that common point is an endpoint of either one of the segments or of both. If a common point of two segments is not an endpoint of either of the segments it is an interior point of both segments.
We will call a common point T of two segments L1 and L2 a true intersection point of L1 and L2 if T is the only common point of L1 and L2 and T is an interior point of both segments.

Consider the three segments L1, L2, and L3:

L1: (27, 44) , (12, 32)
L2: (46, 53) , (17, 62)
L3: (46, 70) , (22, 40)

It can be verified that line segments L2 and L3 have a true intersection point. We note that as the one of the end points of L3: (22,40) lies on L1 this is not considered , be a true point of intersection. L1 and L2 have no common point. So among the three line segments, we find one true intersection point.

Now let us do the same for 5000 line segments. To this end, we generate 20000 numbers using the so-called "Blum Blum Shub" pseudo-random number generator.

s0 = 290797

sn+1 = sn**2 (modulo 50515093)

tn = sn (modulo 500)

To create each line segment, we use four consecutive numbers tn. That is, the first line segment is given by:

(t1, t2) , (t3, t4)

The first four numbers computed according , the above generator should be: 27, 144, 12 and 232. The first segment would thus be (27,144) , (12,232).

How many distinct true intersection points are found among the 5000 line segments?
============================================================
'''
from fractions import Fraction

def bbs(s=290797):
    '''Blum Blum Shub pseudo-random number generator.'''
    while True:
        s = (s * s) % 50515093
        yield s % 500
    
def segment_data(g, n):
    '''Converts an integer number generator into segments.'''
    for _ in xrange(n): yield (g.next(), g.next()), (g.next(), g.next())
    
def tip(((x1, y1), (x2, y2)), ((x3, y3), (x4, y4))):
    '''Return the True Intersection Point (TIP) of two segments (x1, y1) to (x2, y2) and (x3, y3)
    to (x4, y4) if exists, otherwise None.'''
    a, b, c, d, e, f = y3 - y4, x4 - x3, y1 - y2, x2 - x1, x3 - x1, y3 - y1
    s1, t1 = a * e + b * f, c * e + d * f
    if min(s1, t1) <= 0: return None
    else:
        delta = d * a - b * c
        if max(s1, t1) >= delta: return None
        else:
            s = Fraction(s1, delta)
            return (1 - s) * x1 + s * x2, (1 - s) * y1 + s * y2

'''Return the number of distinct TIPs of all segments pairs in the list segments. Brute-force O(n^2)
implementation, where n = #segments.'''
num_tips = lambda segments: len(set(x for x in (tip(L1, L2) for L1 in segments for L2 in segments) if x))

if __name__ == "__main__":
    print num_tips([((27, 44) , (12, 32)),
                    ((46, 53) , (17, 62)),
                    ((46, 70) , (22, 40))]) # 1
    print num_tips(list(segment_data(bbs(), 5000)))
