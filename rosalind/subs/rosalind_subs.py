'''
============================================================
http://rosalind.info/problems/subs

Given: Two DNA strings s and t (each of length at most 1 kbp).

Return: All locations of t as a substring of s. (1-based)
============================================================
'''
from rosalind.rosutil import read_lines

def subs(s, t):
    n, t0, last = len(t), t[0], len(s) - len(t)  # @UnusedVariable
    return [j + 1 for j in (j for (j, sj) in enumerate(s) if j <= last and sj == t0) if s[j:j + n] == t]

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    lines = read_lines('rosalind_subs_sample.dat')
    print ' '.join(map(str, subs(lines[0], lines[1])))
    lines = read_lines('rosalind_subs.dat')
    print ' '.join(map(str, subs(lines[0], lines[1])))
