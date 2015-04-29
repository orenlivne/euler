'''
============================================================
http://www.checkio.org/mission/simple-areas/

Created on Apr 26, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import math

def simple_areas(*args):
    num_args = len(args)
    if num_args == 1: return math.pi * (0.5 * args[0]) ** 2
    if num_args == 2: return args[0] * args[1]
    if num_args == 3:
        s = 0.5 * (args[0] + args[1] + args[2]) 
        return (s * (s - args[0]) * (s - args[1]) * (s - args[2])) ** 0.5
    raise ValueError('Need 1-3 args')

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    def almost_equal(checked, correct, significant_digits=2):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision

    assert almost_equal(simple_areas(3), 7.07), "Circle"
    assert almost_equal(simple_areas(2, 2), 4), "Square"
    assert almost_equal(simple_areas(2, 3), 6), "Rectangle"
    assert almost_equal(simple_areas(3, 5, 4), 6), "Triangle"
    assert almost_equal(simple_areas(1.5, 2.5, 2), 1.5), "Small triangle"
