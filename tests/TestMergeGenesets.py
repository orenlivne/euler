'''
============================================================
Test class Pedigree basic operations. 

Created on May 30, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import time, random, unittest, test_util as tu
from numpy.ma.testutils import assert_equal
from nose.tools import nottest
from examples.merge_genesets import merge_files, hash_file, list_intersection_and_index

class TestMergeGenesets(unittest.TestCase):
    #---------------------------------------------
    # Constants
    #---------------------------------------------
    
    #---------------------------------------------
    # Test Methods
    #---------------------------------------------   
    def __test_intersection(self):
        '''Compare performance of different set intersection implementations.
        frozenset intersection is the fastest.'''
        # Comparing short lists
        a = [1, 2, 3, 4, 5]
        b = [9, 8, 7, 6, 5]
        compare_bitwise(a, b)
        compare_listcomp(a, b)
        compare_intersect(a, b)
        
        # Comparing longer lists
        a = random.sample(xrange(100000), 10000)
        b = random.sample(xrange(100000), 10000)
        compare_bitwise(a, b)
        compare_listcomp(a, b)
        compare_intersect(a, b)

    def test_list_intersection_with_index(self):
        a = [1, 2, 3, 4, 5]
        b = [9, 8, 7, 6, 5, 10, 4, 1]
        result = list_intersection_and_index(a, b)
        assert_equal(list(result), [[1, 0, 7], [4, 3, 6], [5, 4, 4]], 'intersection / indices are wrong')

    def test_hash_file(self):
        result = hash_file(tu.abs_path('misc/geneset1.txt'), ' ', [0, 1])
        assert_equal(result, [(3, 4), (1, 1), (1, 2), (2, 3), (2, 4)], 'file hash is wrong')

    def test_merge_two_files(self):
        result = merge_files(tu.abs_path('misc/geneset1.txt'), tu.abs_path('misc/geneset2.txt'))
        assert_equal(list(result),
                     ['1 2 x2 y2 z3 x2 y2 z8',
                      '2 3 x1 y1 z4 x1 y1 z10',
                      '1 1 x1 y1 z6 x4 y5 z9',
                      '2 4 x2 y2 z5 x2 y2 z12'], 'wrong merge result')
    
    def test_merge_multiple_files(self):
        result = merge_files(tu.abs_path('misc/geneset1.txt'),
                             tu.abs_path('misc/geneset2.txt'),
                             tu.abs_path('misc/geneset3.txt'))
        assert_equal(list(result), ['1 2 x2 y2 z3 x2 y2 z8 x2 y2 z8', '2 3 x1 y1 z4 x1 y1 z10 x1 y1 z10', '2 4 x2 y2 z5 x2 y2 z12 x2 y2 z12'], 'wrong merge result')
    
#---------------------------------------------
# Private Methods
#---------------------------------------------
@nottest
def speed_test(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        for _ in xrange(5000):
            results = func(*args, **kwargs)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2 - t1) * 1000.0)
        return results
    return wrapper

@speed_test
def compare_bitwise(x, y):
    set_x = frozenset(x)
    set_y = frozenset(y)
    return set_x & set_y

@speed_test
def compare_listcomp(x, y):
    return [i for i, j in zip(x, y) if i == j]

@speed_test
def compare_intersect(x, y):
    return frozenset(x).intersection(y)
