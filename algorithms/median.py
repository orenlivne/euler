'''
============================================================
Worst-case O(n) median computation.
============================================================
'''
import numpy as np

def quickselect_ind(a, p, q, k, pivot):
    '''Return the index of a desired rank k in a[p..q-1]. k is 0-based.'''
    print 'quickselect_ind(p=%d, q=%d, k=%d)' % (p, q, k), a[p:q]
    if q == p + 1:
        if k != 0: raise ValueError('We shouldn''t be here')
        return p
    i = pivot(a, p, q)  # Pivot index in p..q-1
    print '  ' , 'pivot: i=%d, x=%.2f' % (i, a[i])
    swap(a, p, i)  # Move pivot to first position in array
    i = partition(a, p, q)  # Partition array to <= pivot, pivot (position i), > pivot groups
    r = i - p  # Rank of x in a[p..q-1]
    print '  ', 'partitioned ', a[p:q]
    print '  ', 'pivot new position: i=%d, new rank r=%d' % (i, r)
    return i if k == r else \
        (quickselect_ind(a, p, i, k, pivot) if k < r else quickselect_ind(a, i + 1, q, k - r - 1, pivot))

def partition(a, p, q):
    '''Partition array to <= pivot, pivot (position i), > pivot groups. Pivot is the first element, a[p].'''
    x, i = a[p], p + 1  # x = pivot
    for j in xrange(p + 1, q):
        if a[j] < x:
            swap(a, i, j)
            i += 1
    swap(a, p, i - 1)  # Move pivot to it final position, straddling the <= and > groups
    return i - 1
    
def swap(a, i, j):
    '''Swap the ith and jth elements in an array a.'''
    if i != j:
        tmp = a[i]
        a[i] = a[j]
        a[j] = tmp

def pivot_group(a, p, q):
    '''Return the index of the median of 5-group medians. a is modified in-place. If #groups is even,
    median is defined here as the element to the left of the center of the medians array.'''
    print 'pivot_group(p=%d, q=%d)' % (p, q), a[p:q]
    n = q - p
    r = n / 5  # Step size for group arrays, also = # groups
    if n % 5: r += 1
    for i in xrange(r):  # Sort each group
        insert_sort(a, 5 * i + p, min(5 * (i + 1) + p, q), r)
    print 'After group sorting', a
    return quickselect_ind(a, 2, min(r + 2, q), r / 2, pivot_group)  # Find median of median array (second element of each group)
    
def insert_sort(a, p=None, q=None, r=1):
    '''Sort a[p,p+r,p+2*r,...,q-r] in place using insert sort. O(n^2) runtime where n = q-p.'''
    if not p: p = 0
    if not q: q = len(a)
    print 'insert_sort(p=%d, q=%d, r=%d)' % (p, q, r), a[p:q:r]
    for i in xrange(p + 1, q, r):
        x, j = a[i], p
        while j < i:  # Find the position j to insert x at
            if a[j] > x:
                for k in xrange(i - 1, j - 1, -1): a[k + 1] = a[k]  # Insert x into its final position - shift elements to right to make space
                a[j] = x
                break
            j += r
    print 'insert_sort result', a[p:q:r]

def pivot_random(a, p, q):
    '''Uniformly-randomly-selected pivot.'''
    return np.random.randint(p, q)

def median(a, pivot=pivot_group):
    '''Return the median of a list/array a.'''
    n = len(a)
    n2 = n / 2
    return a[quickselect_ind(a, 0, n, n2, pivot)] if n % 2 else \
        0.5 * (a[quickselect_ind(a, 0, n, n2, pivot)] + a[quickselect_ind(a, 0, n, n2 - 1, pivot)])

if __name__ == "__main__":
    np.random.seed(1)
    a = np.random.randint(0, 100, 12)
    print median(a, pivot_group)
    print np.median(a)
    print sorted(a)

    a = [72, 9, 75, 5, 37, 8]
    print a
    insert_sort(a)
    print a
