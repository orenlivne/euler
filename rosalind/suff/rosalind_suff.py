'''
============================================================
http://rosalind.info/problems/suff

============================================================
'''
import rosalind.rosutil as ro, rosmatch as rm, numpy as np
from numpy.ma.testutils import assert_equal

def suff(f):
    '''Main driver to solve this problem.'''
    for x in rm.suffix_tree_weights(ro.read_str(f)): print x

#-----------------------------
# Testing
#-----------------------------
def print_suffix_tree_weights(s):
    '''Main driver to solve this problem.'''
    for x in rm.suffix_tree_weights(s): print x

def test_suffix_tree_weights(file_name_prefix):
    s = ro.read_str('%s/%s.dat' % (ro.ROSALIND_HOME, file_name_prefix))
    actual = np.array(list(rm.suffix_tree_weights(s)))
    expected = np.loadtxt('%s/%s.out' % (ro.ROSALIND_HOME, file_name_prefix), dtype=str)
    np.savetxt('%s/%s.mine.out' % (ro.ROSALIND_HOME, file_name_prefix), np.array(sorted(actual)), fmt='%s')
    #print sorted(actual)
    #print sorted(expected) 
    assert_equal(sorted(actual), sorted(expected), 'Wrong suffix tree weight list')

if __name__ == "__main__":
#     for file_name in ('suff/rosalind_suff_sample',
#                       'suff/rosalind_suff_sample1',
#                       'suff/rosalind_suff_sample2',
#                       'suff/rosalind_suff_sample3',
#                       'suff/rosalind_suff_sample4',
#                       'suff/rosalind_suff_data1'):
#         test_suffix_tree_weights(file_name)

    #suff('rosalind_suff_sample.dat')
    suff('rosalind_suff.dat')
