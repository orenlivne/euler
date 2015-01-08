'''
============================================================
http://rosalind.info/problems/orfr

============================================================
'''
import rosalind.rosutil as ro
from rosalind.rosalind_orf import distinct_protein_strings

def orfr(f):
    '''Main driver to solve this problem.'''
    return max((len(x), x) for x in distinct_protein_strings(ro.read_str(f)))[1]

if __name__ == "__main__":
    print orfr('rosalind_orfr_sample.dat')
    print orfr('rosalind_orfr.dat')
