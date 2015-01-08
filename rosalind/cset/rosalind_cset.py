'''
============================================================
http://rosalind.info/problems/cset

Given: An inconsistent character table C on at most 100 taxa.

Return: A submatrix of C' representing a consistent character table on the same taxa and formed by deleting a single row of C. (If multiple solutions exist, you may return any one.)
============================================================
'''
import numpy as np, rosalind.rostree as rt, StringIO
from rosalind.rosalind_chbp import to_newick_tree
from Bio import Phylo
from numpy.ma.testutils import assert_equal

def cset(f):
    '''Main driver to solve this problem.'''
    c = rt.load_character_set(f)
    return remove_inconsistent_row(c)

def remove_inconsistent_row(c):
    '''Main driver to solve this problem.'''
    s = np.array(['a%d' % (x,) for x in xrange(c.shape[1])])  # Dummy
    #print c.shape
    for i in xrange(c.shape[0]):
        c_copy = np.delete(c, i, 0)
        try:
            #print 'i', i
            t = to_newick_tree(c_copy, s)
            #print 't', t
            #print c_copy
            #print to_binary_string(c)  # np.savetxt(sys.stdout, c_copy, fmt='%d', delimiter='')
            return c_copy, t
        except ValueError: pass 

def test_char_set(file_name):    
    c, t_str = cset(file_name)
    t = Phylo.read(StringIO.StringIO(t_str), 'newick')
    # Phylo.draw_ascii(t)
    assert_equal(rt.standardize_char_table(c), rt.char_table(t), 'Original character set minus removed row not reproduced from tree')

if __name__ == "__main__":
    print cset('rosalind_cset.dat')[1]
    test_char_set('rosalind_cset.dat')
    # Compare with c: sort both by row, standardize so that #0's <= #1's
    # cset('rosalind_cset.dat')
    # print char_set_binary_string(c)
