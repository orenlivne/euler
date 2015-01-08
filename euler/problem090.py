'''
============================================================
http://projecteuler.net/problem=90

Each of the six faces on a cube has a different digit (0 to 9) written on it; the same is done to a second cube. By placing the two cubes side-by-side in different positions we can form a variety of 2-digit numbers.

For example, the square number 64 could be formed:


In fact, by carefully choosing the digits on both cubes it is possible to display all of the square numbers below one-hundred: 01, 04, 09, 16, 25, 36, 49, 64, and 81.

For example, one way this can be achieved is by placing {0, 5, 6, 7, 8, 9} on one cube and {1, 2, 3, 4, 8, 9} on the other cube.

However, for this problem we shall allow the 6 or 9 to be turned upside-down so that an arrangement like {0, 5, 6, 7, 8, 9} and {1, 2, 3, 4, 6, 7} allows for all nine square numbers to be displayed; otherwise it would be impossible to obtain 09.

In determining a distinct arrangement we are interested in the digits on each cube, not the order.

{1, 2, 3, 4, 5, 6} is equivalent to {3, 6, 4, 1, 2, 5}
{1, 2, 3, 4, 5, 6} is distinct from {1, 2, 3, 4, 5, 9}

But because we are allowing 6 and 9 to be reversed, the two distinct sets in the last example both represent the extended set {1, 2, 3, 4, 5, 6, 9} for the purpose of forming 2-digit numbers.

How many distinct arrangements of the two cubes allow for all of the square numbers to be displayed?
============================================================
'''
from itertools import combinations, product

SIX_NINE = set([6, 9])
SQUARES = [(x / 10, x % 10) for x in (x * x for x in xrange(1, 10))]
DIGITS = list(set(range(10))) 
extend = lambda s: s | SIX_NINE if 6 in s or 9 in s else s
cubes_ok = lambda s0, s1, X: all(x[0] in s0 and x[1] in s1 or x[1] in s0 and x[0] in s1 for x in X)

if __name__ == "__main__":
    print SQUARES
    s0, s1 = set([0, 5, 6, 7, 8, 9]),set([1, 2, 3, 4, 8, 9])
    print list(s0), list(s1), extend(s0), extend(s1), cubes_ok(extend(s0), extend(s1), SQUARES)

    print sum(1 for s0, s1 in ((set(s0), set(s1)) for s0, s1 in 
                              product(combinations(DIGITS, 6), combinations(DIGITS, 6)))
              if list(sorted(s0)) <= list(sorted(s1)) and cubes_ok(extend(s0), extend(s1), SQUARES))
