'''
============================================================
http://rosalind.info/problems/pdpl

Given: A multiset L containing (n2) positive integers for some positive integer n.

Return: A set X containing n nonnegative integers such that DELTA(X)=L.
============================================================
'''
import rosalind.rosutil as ro
from collections import Counter
from numpy.ma.testutils import assert_equal

multi_diff_scalar_set = lambda y, X: Counter(ro.iabs(x - y) for x in X)
multi_diff_self = lambda X: Counter(x - y for x in X for y in X if y < x)

def pdpl(f):
    L = restriction_map(ro.read_ints_str(f))
    return ro.join_list(sorted(L))  # Main driver to solve this problem.

def restriction_map(L):
    d = max(L)
    # print len(L)
    n = int(0.5 * (1 + (1 + 8 * len(L)) ** 0.5))
    # print 'n', n
    return place(Counter(L) - Counter([d]), set([d, 0]), d, n)

def subseteq(a, b):
    '''Is a subset or equal to b, for a, b Counters.'''
    return set(a.keys()) <= set(b.keys()) and all(a[i] <= b[i] for i in a)
                         
SEP = ' '
MAX_DEPTH = 0
def place(L, X, xn, n, depth=0):
    '''Skiena\'s back-tracking algorithm.'''
    if depth < MAX_DEPTH:
        print SEP * depth, '|X|', len(X), '|L|', sum(L.itervalues())
        print SEP * depth, 'L', L
        print SEP * depth, 'X', X  
    if not L: return X
    # if len(X) > n: raise ValueError('WARNING: we should not be here, X too long')  # raise ValueError('We should not be here, X too long')
    y = max(L)
    for z in (xn - y, y):
        if z not in X:
            d = multi_diff_scalar_set(z, X)
            if depth < MAX_DEPTH:
                print SEP * depth, 'z', z
                print SEP * depth, 'd', d
            if subseteq(d, L):  # d <= L:  # Recurse
                retval = place(L - d, X | set([z]), xn, n, depth=depth + 1)
                if retval: return retval

def test_restriction_map(X):
    print X
    X = sorted(X)
    L = multi_diff_self(X)
    Y = sorted(restriction_map(ro.flatten_counter(L)))
    DY = multi_diff_self(Y)
    assert_equal(L, DY, 'Wrong restriction map')
    print 'OK'

if __name__ == "__main__":
    # test_restriction_map([0, 2, 4, 7, 10])
    # test_restriction_map([0, 2, 4, 8, 10])
    # test_restriction_map([0, 2, 5, 6, 15, 17])
    # test_restriction_map([12, 14, 27, 34, 69, 72, 77, 82, 96])
    # test_restriction_map([ 0, 3, 15 , 29, 61, 81])
    # test_restriction_map(np.unique(np.random.randint(0, 100, 7)))
    # print pdpl('rosalind_pdpl_sample.dat')
    print pdpl('rosalind_pdpl.dat')
