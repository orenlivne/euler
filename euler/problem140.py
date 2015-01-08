'''
============================================================
http://projecteuler.net/problem=140

Consider the infinite polynomial series AG(x) = xG1 + x2G2 + x3G3 + ..., where Gk is the kth term of the second order recurrence relation Gk = Gk1 + Gk2, G1 = 1 and G2 = 4; that is, 1, 4, 5, 9, 14, 23, ... .

For this problem we shall be concerned with values of x for which AG(x) is a positive integer.

The corresponding values of x for the first five natural numbers are shown below.

x    AG(x)
(51)/4    1
2/5    2
(222)/6    3
(1375)/14    4
1/2    5
We shall call AG(x) a golden nugget if x is rational, because they become increasingly rarer; for example, the 20th golden nugget is 211345365.

Find the sum of the first thirty golden nuggets.
============================================================
'''
from problem094 import pell_solutions
import itertools as it

A0 = it.chain([(7, 1)], ((7 * x + 5 * y, 7 * y + x) for x, y in it.islice(pell_solutions(5), 1, None, 2)))
A1 = ((7 * x - 5 * y, 7 * y - x) for x, y in it.islice(pell_solutions(5), 1, None, 2))
B0 = ((15 * z + y, 3 * y + z) for y, z in it.islice(pell_solutions(5, -1), 0, None, 2))
B1 = ((15 * z - y, 3 * y - z) for y, z in it.islice(pell_solutions(5, -1), 1, None, 2))
C0 = ((2 * (4 * x + 5 * y), 2 * (4 * y + x)) for x, y in it.islice(pell_solutions(5), 0, None, 2))
C1 = ((2 * (4 * x - 5 * y), 2 * (4 * y - x)) for x, y in it.islice(pell_solutions(5), 0, None, 2))

if __name__ == "__main__":
    print sum(it.imap(lambda (c, _):(c - 7) / 5, it.islice(it.chain.from_iterable(it.izip(A0, B0, C1, C0, B1, A1)), 1, 31)))
    
