'''
============================================================
http://www.checkio.org/mission/count-inversions/

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def mergesort(a):
    '''Sorts the array a in non-decreasing order. Also return the number of inversions in the array.'''
    n = len(a)
    if n == 1: return a, 0
    left, num_inversions_left = mergesort(a[:n / 2])
    right, num_inversions_right = mergesort(a[n / 2:])
    merged = list(merge(left, right))
    return merged[:-1], num_inversions_left + num_inversions_right + merged[-1]

def merge(a, b):
    '''Merges two non-decreasing lists into one non-decreasing list. Also return the number of
    inversions in the array.'''
    i, j, na, nb, num_inversions = 0, 0, len(a), len(b), 0
    while i < na and j < nb:
        min_a, min_b = a[i], b[j]
        if min_a < min_b:
            yield min_a
            i += 1
        else:
            num_inversions += (na - i)
            yield min_b
            j += 1
    i, a = (j, b) if i == na else (i, a)
    for k in xrange(i, len(a)): yield a[k]
    yield num_inversions

def count_inversion(sequence):
    """
        Count inversions in a sequence of numbers
    """
    return mergesort(sequence)[1]

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert count_inversion((1, 2, 5, 3, 4, 7, 6)) == 3, "Example"
    assert count_inversion((0, 1, 2, 3)) == 0, "Sorted"
    assert count_inversion((99, -99)) == 1, "Two numbers"
    assert count_inversion((5, 3, 2, 1, 0)) == 10, "Reversed"
