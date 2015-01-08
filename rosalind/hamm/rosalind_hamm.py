'''
============================================================
http://rosalind.info/problems/hamm

Given: Two DNA strings s and t of equal length (not exceeding 1 kbp).

Return: The Hamming distance dH(s,t).
============================================================
'''
import rosalind.rosutil as ro

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print ro.hamm(*ro.read_lines('rosalind_hamm_sample.dat'))
    print ro.hamm(*ro.read_lines('rosalind_hamm.dat'))
