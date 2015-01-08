'''
============================================================
http://rosalind.info/problems/bins

Problem
The problem is to find a given set of keys in a given array.

Given: Two positive integers n<=10**5 and m<=10**5, a sorted
array A[1..n] of integers from -10**5 to 10**5 and a list of
m integers -10**5<=k1,k2,...,km<=10**5.

Return: For each ki, output an index 1<=j<=n s.t. A[j]=ki or
"-1" if there is no such index.
============================================================
'''
import rosalind.rosutil as ro

'''Return value from binary search for a value that was not found.'''
NOT_FOUND = -1

'''Convert 0-based to 1-based index.'''
to_one_based = lambda i: NOT_FOUND if i == NOT_FOUND else (i + 1)
  
def bin_search(a, v):
    '''Return the (an) index of v in the list a, or NOT_FOUND if not found.'''
    low, high = 0, len(a) - 1
    while high >= low:
        mid = (low + high) / 2
        a_mid = a[mid]
        if v == a_mid: return mid
        elif v < a_mid: high = mid - 1
        else: low = mid + 1
    return NOT_FOUND

def bins(f):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    a, k = ro.to_int_list(lines[2]), ro.to_int_list(lines[3])
    for v in k: print '%s ' % (to_one_based(bin_search(a, v))),
    print ''

if __name__ == "__main__":
    bins('rosalind_bins_sample.dat')
    bins('rosalind_bins.dat')
