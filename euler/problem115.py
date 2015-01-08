'''
============================================================
http://projecteuler.net/problem=115

NOTE: This is a more difficult version of problem 114.

A row measuring n units in length has red blocks with a minimum length of m units placed on it, such that any two red blocks (which are allowed to be different lengths) are separated by at least one black square.

Let the fill-count function, F(m, n), represent the number of ways that a row can be filled.

For example, F(3, 29) = 673135 and F(3, 30) = 1089155.

That is, for m = 3, it can be seen that n = 30 is the smallest value for which the fill-count function first exceeds one million.

In the same way, for m = 10, it can be verified that F(10, 56) = 880711 and F(10, 57) = 1148904, so n = 57 is the least value for which the fill-count function first exceeds one million.

For m = 50, find the least value of n for which the fill-count function first exceeds one million.
============================================================
'''
import itertools as it

def fill_count(m):
    '''Yield F(m,n) for n=0,1,2,... . Works for any m>=3.'''
    p, f = m + 1, [1] * m + [2]
    for x in f: yield x
    for n in it.count():
        i = n % p
        f[i] += (2 * f[(n - 1) % p] - f[(n - 2) % p])
        yield f[i]

'''Return the smallest n for which F(m,n) > L.'''
first_n = lambda m, L: it.dropwhile(lambda x: x[1] <= L, enumerate(fill_count(m))).next()[0]

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print list(it.islice(fill_count(2), 5))
    print list(it.islice(fill_count(3), 50, 51))[0]  # Answer to problem114
    print first_n(50, 10 ** 6)
