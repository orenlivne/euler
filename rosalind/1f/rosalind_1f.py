'''
============================================================
http://rosalind.info/problems/1f

Find all approximate occurrences of a pattern in a string.

Given: Two strings Pattern and Text along with an integer d.

Return: All positions where Pattern appears in Text with at most d mismatches.
============================================================
'''
import rosalind.rosutil as ro

def apm(s, p, d):
    '''Return a list of all positions where p appears in s with at most d mismatches.'''
    m = len(p)
    return [i for i in xrange(len(s) - m) if ro.hamm(s[i:i + m], p) <= d]

def one_f(f):
    p, s, d = ro.read_lines(f)
    return ro.join_list(apm(s, p, int(d)))

if __name__ == "__main__":
    print one_f('rosalind_1f_sample.dat')
    print one_f('rosalind_1f.dat')
