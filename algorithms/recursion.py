'''
============================================================
Recursion Chapter in Programming Exposed Book.
============================================================
'''
import itertools as it

def _binary_search(array, lower, upper, target):
    '''Binary search in the sorted array ''array''.
    Searches for the value target in array[lower..upper].'''
    # Boundary case
    if upper - lower == 1: return lower if target == array[lower] else -1
    # Divide-and-conquer
    middle = (lower + upper) / 2
    x = array[middle]
    return middle if target == x else (_binary_search(array, lower, middle, target) if target < x \
        else _binary_search(array, middle + 1, upper, target))

def _binary_search_nr(array, lower, upper, target):
    '''Non-recursive counterpart of _binary_search. of Binary search in the sorted array ''array''.
    Searches for the value target in array[lower..upper].'''
    while True:
        # Boundary case
        if upper - lower == 1: return lower if target == array[lower] else -1
        # Divide-and-conquer
        middle = (lower + upper) / 2
        x = array[middle]
        if target == x: return middle 
        else: lower, upper = (lower, middle) if target < x else (middle + 1, upper)

'''Wrapper method. Searches for the value target in the array ''array''.'''
# Boundary case of strange input (empty array)
binary_search = lambda array, target: _binary_search_nr(array, 0, len(array), target) if array else -1

'''Permutations and combinations, in particular of strings.'''
str_result = lambda a: (''.join(p) for p in a)

def permutations(a):
    '''Return all permutations of an list a.'''
    n = len(a)
    if n == 1: yield (a,)
    for i in xrange(n):
        prefix = (a[i],)
        for p in permutations(a[:i] + a[i + 1:]): yield prefix + p

def _combinations(a):
    '''Return all non-empty combinations in lexicographic order.'''
    yield ()  # No element in first position of the combination
    for i in xrange(len(a)):  # Put each element in first position of the combination. Combinations are sorted so the first element must be followed by larger elements.
        prefix = (a[i],)
        for c in _combinations(a[i + 1:]): yield prefix + c

'''Return all non-empty combinations in lexicographic order.'''
combinations = lambda a: it.islice(_combinations(sorted(a)), 1, None)

#-----------------------
# Telephone words
#-----------------------
def counter(b):
    '''A running counter [i[0],...,i[n-1]] where 0<=i[j]<b[j] for 0<=j<len(b). Outputs iterates in
    lexicographic order. (Less efficient than Gray code).'''
    n = len(b)
    c, i = [0] * n, n - 1
    while True:
        yield tuple(c)
        c[i] += 1
        while c[i] == b[i]:  # Overflow, search for position to the left of i that does not overflow
            c[i] = 0 # When we carry over, all counters to the right are zeroed out
            i -= 1
            if i < 0: return  # No such position found ==> done
            c[i] += 1
        i = n - 1
            
def tel_words(x, d):
    letters = [d[y] for y in map(int, str(x))]
    n = len(letters)
    return (''.join(letters[i][c[i]] for i in xrange(n)) for c in counter(map(len, letters)))

# _A = ord('A')
# TEL_LETTERS = dict([(y, str(y)) for y in (0, 1)] + [(y, ''.join(chr(_A + z) for z in xrange(3 * (y - 2), 3 * (y - 1)))) for y in xrange(2, 10)])
TEL_LETTERS = {0: '0', 1: '1', 2: 'ABC', 3: 'DEF', 4: 'GHI', 5: 'JKL', 6: 'MNO', 7: 'PRS', 8: 'TUV', 9: 'WXY'}

#-----------------------
# Tests        
#-----------------------
import unittest
from numpy.ma.testutils import assert_equal

class TestRecursion(unittest.TestCase):
    #---------------------------------------------
    # Test Methods
    #---------------------------------------------
    def test_binary_search(self):
        assert_equal(binary_search([], 0), -1)
        assert_equal(binary_search([-1], -1), 0)
        assert_equal(binary_search([-1, 2], 2), 1)
        assert_equal(binary_search([-1, 2, 5], 5), 2)
        assert_equal(binary_search([-1, 2, 5, 8, 16, 24], 8), 3)
        assert_equal(binary_search([-1, 2, 5, 8, 16, 24, 30], 8), 3)
        assert_equal(binary_search([-1, 2, 5, 8, 16, 24, 30], -1), 0)
        assert_equal(binary_search([-1, 2, 5, 8, 16, 24, 30], 0), -1)
        assert_equal(binary_search([-1, 2, 5, 8, 8, 24, 30], 8) in frozenset([3, 4]), True)  # Arbitrary index returned if item occurs multiple times
    
    def test_permutations(self):
        s = 'abcd'
        assert_equal(set(str_result(permutations(s))), set(str_result(it.permutations(s))))
        s = 'a'
        assert_equal(set(str_result(permutations(s))), set(str_result(it.permutations(s))))
    
    def test_combinations(self):
        # Test that we get the right combinations in the expected order (lexicographically sorted)
        s = 'wxyz'
        assert_equal(list(str_result(combinations(s))), sorted(it.chain.from_iterable(str_result(it.combinations(s, r)) for r in xrange(1, len(s) + 1))))
        s = 'w'
        assert_equal(list(str_result(combinations(s))), sorted(it.chain.from_iterable(str_result(it.combinations(s, r)) for r in xrange(1, len(s) + 1))))

    def test_tel_words(self):
        b = (3, 1, 3)
        assert_equal(list(counter(b)), list(it.product(*(xrange(x) for x in b))))
        x = 4971927
        assert_equal(list(tel_words(x, TEL_LETTERS)), list(it.imap(lambda y: ''.join(y), it.product(*(TEL_LETTERS[y] for y in map(int, str(x)))))))

# if __name__ == "__main__":
#     pass
