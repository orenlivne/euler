'''
============================================================
http://rosalind.info/problems/rstr

Given: A positive integer N <= 100000, a number x between 0 and 1, and a DNA string s of length at most 10 bp.

Return: The probability that if N random DNA strings having the same
length as s are constructed with GC-content x (see "Introduction to Random Strings"),
then at least one of the strings equals s. We allow for the same random string to be created
more than once.
============================================================
'''
import rosalind.rosutil as ro

def p(N, x, s):
    g = ro.gc_count(s)
    return 1 - (1 - (0.5 * x) ** g * (0.5 * (1 - x)) ** (len(s) - g)) ** N

def rstr(f):
    lines = ro.read_lines(f)
    parts = lines[0].split()
    return p(int(parts[0]), float(parts[1]), lines[1])

if __name__ == "__main__":
    print rstr('rosalind_rstr_sample.dat')
    print rstr('rosalind_rstr.dat')
