'''
============================================================
http://projecteuler.net/problem=15

Starting in the top left corner of a 2x2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

How many such routes are there through a 20x20 grid?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import scipy.special

def num_paths_grid(n):
    '''Number of paths between corners of an nxn grid.

    >>> num_paths_grid(2)
    6

    >>> num_paths_grid(20)
    137846528819L
    ''' 
    return int(scipy.special.binom(2 * n, n))

# TODO: add dynamic programming implementation 

if __name__ == "__main__":
    import doctest
    doctest.testmod()
