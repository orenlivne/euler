'''
============================================================
http://rosalind.info/problems/loca

A local alignment of two strings s and t is an alignment of
substrings r and u of s and t, respectively. Let opt(r,u)
denote the score of an optimal alignment of r and u with
respect to some predetermined alignment score.

Given: Two protein strings s and t in FASTA format (each
having length at most 1000 aa).

Return: A maximum alignment score along with substrings r
and u of s and t, respectively, which produce this maximum
alignment score (multiple solutions may exist, in which case
you may output any one). Use:

The PAM250 scoring matrix.
Linear gap penalty equal to 5.
============================================================
'''
import rosalind.rosutil as ro, rosalign as ra

def loca(f, debug=False):
    '''Main driver to solve the LOCA problem.'''
    x, y = ro.fafsa_values(f)
    d, (xx, yy) = ra.optimal_alignment(x, y, ra.PAM250, -5, -5, align='local', debug=debug, gap_symbol='')
    return ro.join_list((d, xx, yy), delimiter='\n')

if __name__ == "__main__":
    print loca(ro.ROSALIND_HOME + '/loca/rosalind_loca_sample.dat')
    print loca(ro.ROSALIND_HOME + '/loca/rosalind_loca.dat')
