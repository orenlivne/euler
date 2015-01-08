'''
============================================================
http://projecteuler.net/problem=142

Find the smallest x + y + z with integers x  y  z  0 such that x + y, x  y, x + z, x  z, y + z, y  z are all perfect squares.
============================================================
'''
from itertools import count

def is_sqr(x):
    y = x ** 0.5
    return y - int(y) < 1e-12

def min_xyz(s_bound=None):
    '''Based on http://blog.san-ss.com.ar/2011/12/project-euler-problem-142-solved.html , but
    modified to ensure correctness. Performs two passes to find the minimum s=x+y+z:
    1) obtain lower bound for the minimum s.
    2) Verify that there exists no s < s_min (or return that value).''' 
    s_min = 0
    for a in xrange(3, s_bound + 1) if s_bound else count(3):
        a2 = a * a
        # f must be even since y is even. f's range is bounded so that x+z = a2-f2 > 0.
        for f in (f for f in xrange(2, a, 2) if is_sqr(a2 - f * f)):
            f2 = f * f
            c2 = a2 - f2
            # e must be even since z is even. e's range is bounded so that x > y. 
            for e in (e for e in xrange(f + 2, int(c2 ** 0.5), 2) if is_sqr(a2 - e * e) and is_sqr(c2 - e * e)):
                s = a2 + (e * e - f2) / 2
                if s_bound is None: return s  # Pass 1: s = lower bound on the minimum s 
                elif s_min == 0 or s < s_min: s = s_min  # Pass 2 (verification) 
    return s_min  # Can only get here in pass 2 - final result

if __name__ == "__main__":
    print min_xyz()  # 1006193

# Inspired by
# def min_xyz_ss():
#     for a in count(6):
#         a_2 = a ** 2
#         for f in (f for f in takewhile(lambda f: f < a, count(4)) if is_sqr(a_2 - f ** 2)):
#             f_2 = f ** 2
#             c_2 = a_2 - f_2
#             setoff = 3 if (f & 1) else 2
#             for e in (e for e in takewhile(lambda e: e ** 2 < c_2, count(setoff, 2)) if is_sqr(c_2 - e ** 2) and is_sqr(a_2 - e ** 2)):
#                 e_2 = e ** 2
#                 b_2 = c_2 - e_2
#                 d_2 = a_2 - e_2
#                 if c_2 > d_2:
#                     z = -(d_2 - c_2) // 2
#                     y = -(-d_2 - c_2 + 2 * b_2) // 2
#                     x = (d_2 + c_2) // 2
#                     print('The result is: (x){0} + (y){1} + (z){2} = {3}'.format(x, y, z, x + y + z))
#                     return x + y + z
