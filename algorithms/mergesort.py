'''
============================================================
Merge sort: O(n log n) time.
============================================================
'''
def mergesort(a):
    '''Sorts the array a in non-decreasing order.'''
    n = len(a)
    return a if n == 1 else list(merge(mergesort(a[:n / 2]), mergesort(a[n / 2:])))  # Note: the two sub-sorts can be performed in parallel!

def merge(a, b):
    '''Merges two non-decreasing lists into one non-decreasing list.'''
    i, j, na, nb = 0, 0, len(a), len(b)
    while i < na and j < nb:
        min_a, min_b = a[i], b[j]
        if min_a < min_b:
            yield min_a
            i += 1
        else:
            yield min_b
            j += 1
    i, a = (j, b) if i == na else (i, a)
    for k in xrange(i, len(a)): yield a[k]
    
if __name__ == "__main__":
    import timeit, numpy as np
    for n in 2 ** np.arange(20):
        print n, timeit.timeit(stmt='mergesort(a)',
                               setup='import numpy as np; from __main__ import mergesort; \
                               a = np.random.randint(0, %d, %d)' % (n, n), number=1)
