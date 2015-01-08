'''
============================================================
http://rosalind.info/problems/rvco

Recall that in a DNA string s, 'A' and 'T' are complements of each other, as are 'C' and 'G'. Furthermore, the reverse complement of s is the string sc formed by reversing the symbols of s and then taking the complement of each symbol (e.g., the reverse complement of "GTCA" is "TGAC").

The Reverse Complement program from the SMS 2 package can be run online here.

Given: A collection of n (n<=10) DNA strings.

Return: The number of given strings that match their reverse complements.
============================================================
'''
import rosalind.rosutil as ro

def rvco(f):
    '''Main driver to solve this problem.'''
    return sum(1 for x in ro.fafsa_itervalues(f) if x == ro.revc(x))

if __name__ == "__main__":
    print rvco('rosalind_rvco_sample.dat')
    print rvco('rosalind_rvco.dat')
