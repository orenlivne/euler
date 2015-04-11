'''
============================================================
http://www.checkio.org/mission/humpty-dumpty/

Created on Apr 5, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import math

def checkio(height, width):
    c, a = height / 2., width / 2.
    v = (4 * math.pi * a * a * c) / 3.
    if c < a:
        # Oblate
        e = (1. - float(c * c) / (a * a)) ** 0.5
        s = 2 * math.pi * a * a * (1 + (1 - e * e) * math.atanh(e) / e)
    elif abs(c - a) < 1e-16:
        # Sphere
        s = 4 * math.pi * a * a
    else:
        # Prolate
        e = (1. - float(a * a) / (c * c)) ** 0.5
        s = 2 * math.pi * a * a * (1 + c * math.asin(e) / (a * e))
    return v, s

# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    def check_case((a, b), expected):
        actual = checkio(a, b)
        assert (sum(abs(x - y) for x, y in zip(actual, expected)) < 1e-2)
         
    check_case((2, 2), [4.19, 12.57])  # , "Sphere"
    check_case((4, 2), [8.38, 21.48])  # , "Prolate spheroid"
    check_case((2, 4), [16.76, 34.69])  # , "Oblate spheroid"
