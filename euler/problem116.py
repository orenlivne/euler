'''
============================================================
http://projecteuler.net/problem=116

A row of five black square tiles is to have a number of its tiles replaced with coloured oblong tiles chosen from red (length two), green (length three), or blue (length four).

If red tiles are chosen there are exactly seven ways this can be done.
If green tiles are chosen there are three ways.
And if blue tiles are chosen there are two ways.

Assuming that colours cannot be mixed there are 7 + 3 + 2 = 12 ways of replacing the black tiles in a row measuring five units in length.

How many different ways can the black tiles in a row measuring fifty units in length be replaced if colours cannot be mixed and at least one coloured tile must be used?

NOTE: This is related to problem 117.
============================================================
'''
import itertools as it

def fill_count(m):
    '''F(m,n) for n=0,1,2,...; m >= 2. Includes all-black tiles.'''
    f, i = [1] * m, 0  # (BC)
    for x in f: yield x
    for n in it.count():  # Since we start at n=m <-> i=0, it works to start at n=0 as the count() arg
        i = n % m
        f[i] += f[(i - 1) % m]  # Eq. (1)
        yield f[i]
        
block_exists = lambda x: x - 1
choice_fill_count = lambda M: it.imap(sum, it.izip(*(it.imap(block_exists, fill_count(m)) for m in M)))

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print it.islice(choice_fill_count([2, 3, 4]), 50, 51).next()
