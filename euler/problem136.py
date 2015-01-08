'''
============================================================
http://projecteuler.net/problem=136

The positive integers, x, y, and z, are consecutive terms of an arithmetic progression. Given that n is a positive integer, the equation, x2  y2  z2 = n, has exactly one solution when n = 20:

132  102  72 = 20

In fact there are twenty-five values of n below one hundred for which the equation has a unique solution.

How many values of n less than fifty million have exactly one solution?
============================================================
'''
import numpy as np
from euler.problem135 import num_solutions
from euler.problem146 import isp

if __name__ == "__main__":
    # Testing, problem 136
    a = np.where(num_solutions(300) == 1)[0]
    print a
    m = map(lambda x: x / 4, filter(lambda x: not isp(x), a))
    print m
    print filter(lambda x: x >= 3 and not isp(x), m)

    print len(np.where(num_solutions(5 * 10 ** 7) == 1)[0])
