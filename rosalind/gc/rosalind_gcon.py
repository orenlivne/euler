'''
============================================================
http://rosalind.info/problems/glob (gap = b*L)
http://rosalind.info/problems/gcon (gap = a)
http://rosalind.info/problems/gaff (gap = a + b*(L-1))

In a constant gap_ext penalty, every gap_ext receives some predetermaxed constant penalty, regardless of its length. Thus, the insertion or deletion of 1000 contiguous symbols is penalized equally to that of a single symbol.

Given: Two protein strings s and t in FASTA format (each of length at most 1000 aa).

Return: The maximum alignment score between s and t. Use:

The BLOSUM62 scoring matrix. Constant gap_ext penalty equal to 5.
============================================================
'''
import rosalind.rosutil as ro, rosalign as ra

def glob(f, debug=False):
    '''Main driver to solve the GLOB problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = ra.optimal_alignment(x, y, ra.BLOSUM62, -5, -5, debug=debug)
    print d
    print xx
    print yy
    return d

def gcon(f, debug=False):
    '''Main driver to solve the GCON problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = ra.optimal_alignment(x, y, ra.BLOSUM62, -5, 0, debug=debug)
    print d
    print xx
    print yy
    return d

def gaff(f, score=ra.BLOSUM62, gap_init= -11, gap_ext= -1, debug=False):
    '''Main driver to solve the GAFF problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = ra.optimal_alignment(x, y, score, gap_init, gap_ext, debug=debug)
    print d
    print xx
    print yy

if __name__ == "__main__":
    glob('rosalind_glob_sample.dat')
    gcon('rosalind_gcon_sample.dat')
    gaff('rosalind_gaff_sample.dat')

    glob('rosalind_glob.dat')
    gcon('rosalind_gcon.dat')
    gaff('rosalind_gaff_data6.dat')
