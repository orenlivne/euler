'''
============================================================
http://projecteuler.net/problem=220

Let D0 be the two-letter string "Fa". For n >= 1, derive Dn from Dn-1 by the string-rewriting rules:

"a" -> "aRbFR"
"b" ->"LFaLb"

Thus, D0 = "Fa", D1 = "FaRbFR", D2 = "FaRbFRRLFaLbFR", and so on.

These strings can be interpreted as instructions to a computer graphics program, with "F" meaning "draw forward one unit", "L" meaning "turn left 90 degrees", "R" meaning "turn right 90 degrees", and "a" and "b" being ignored. The initial position of the computer cursor is (0,0), pointing up towards (0,1).

Then Dn is an exotic drawing known as the Heighway Dragon of order n. For example, D10 is shown below; counting each "F" as one step, the highlighted spot at (18,16) is the position reached after 500 steps.


What is the position of the cursor after 1012 steps in D50 ?
Give your answer in the form x,y with no spaces.
============================================================
'''
from itertools import islice
from math import log
from problem036 import base_digits

base_str = lambda n, b: ''.join(str(x) for x in reversed(base_digits(n, b)))
largest_m_le = lambda N, k : int(log(N / k) / log(2))

def dragon_curve((x, y)=(0, 0), (a, b)=(0, 1)):
    '''Yield the coordinates, directions and step numbers of the dragon curve after each step,
    starting at (x,y) with direction (a,b).'''
    n = 0
    yield (x, y), (a, b), n
    while True:
        x += a; y += b
        n += 1
        s = (((n & -n) << 1) & n) != 0
        a, b = (-b if s else b), (a if s else -a)
        yield (x, y), (a, b), n

def x_coef(k):
    '''Return the c's of m (mod 4)=0,1,2,3 in x(k*2**m) = c*(-4)*([k/4]).'''
    m, ns, c, d_prev = 0, k, [], None
    for x, d, n in dragon_curve():
        if n == ns:
            fac = (-4) ** (m / 4)
            if m >= 4:
                # print 'm %-2d n %-8d %-24s (%+4d,%+4d) (%+d,%+d) %.3f %.3f' % \
                # (m, n, base_str(n, 2), x[0], x[1], d[0], d[1], 1.*x[0] / fac, 1.*x[1] / fac)
                if d_prev and d != d_prev: raise ValueError('Non-constant direction')
                d_prev = d
                c.append((x[0] / fac, x[1] / fac))
                                
            m += 1
            ns *= 2
            if m == 8: return d, c

def dragon_curve_coord_at_step(N, L):
    '''Return the coordinates after N steps in the dragon curve in the format "x,y".'''
    # Extrapolate the value of x from the pattern of numbers n who start with the same L binary
    # digits as N into the largest number of this form that's <= N 
    k = int(base_str(N, 2)[:L], 2)
    m = largest_m_le(N, k)
    d, c = x_coef(k)
    cx, cy = c[m % 4]
    fac = (-4) ** (m / 4)
    steps = N - k * 2 ** m
    # print 'k 2^m', k * 2 ** m, 'm', m, 'm % 4', m % 4, 'steps', steps, 'start', (cx, cy), (cx * fac, cy * fac), d
    # Trace the rest of the dragon curve - brute-force
    return ','.join(map(str, islice(dragon_curve((cx * fac, cy * fac), d), steps, steps + 1).next()[0]))
    
if __name__ == "__main__":
    print dragon_curve_coord_at_step(10 ** 12, 14)
