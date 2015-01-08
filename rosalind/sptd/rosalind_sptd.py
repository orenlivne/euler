'''
============================================================
http://rosalind.info/problems/sptd

Given: An inconsistent character table C on at most 100 taxa.

Return: A submatrix of C' representing a consistent character table on the same taxa and formed by deleting a single row of C. (If multiple solutions exist, you may return any one.)
============================================================
'''
import rosalind.rosutil as ro, rostree as rt

def sptd(f):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    return rt.dist_split(rt.read_newick_str(lines[1]), rt.read_newick_str(lines[2]), lines[0].split())

if __name__ == "__main__":
    print sptd('rosalind_sptd_sample.dat')
    print sptd('rosalind_sptd.dat')
