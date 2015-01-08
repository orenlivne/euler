'''
============================================================
http://projecteuler.net/problem=28

Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
============================================================
'''
def spiral_diagonal_sum(n):
    '''Return the (2*n+1)x(2*n+1) spiral diagonals sum.
    
    5x5 spiral:
    >>> spiral_diagonal_sum(2)
    101

    1001x1001 spiral:
    >>> spiral_diagonal_sum(500)
    669171001'''
    return 1 + 4 * (2 * n * (n + 1) * (2 * n + 1) / 3 + n * (n + 1) / 2 + n)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
