'''
============================================================
http://rosalind.info/problems/revc

Given: A DNA string s of length at most 1000 bp.
Return: The reverse complement sc of s.
============================================================
'''
from rosalind.rosutil import read_str, revc

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
#    print revc(read_str('rosalind_revc_sample.dat'))
#    print revc(read_str('rosalind_revc.dat'))
    print revc(read_str('rosalind_revc_1b.dat'))
