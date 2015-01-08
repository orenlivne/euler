'''
============================================================
http://rosalind.info/problems/1g

Find the most frequent k-mers with mismatches in a string.

Given: A string Text as well as integers k and d.

Return: All most frequent k-mers with up to d mismatches in Text.
============================================================
'''
import rosalind.rosutil as ro

def one_g(f):
    '''Main driver for solving this problem.'''
    lines = ro.read_lines(f)
    s, (k, d) = lines[0], map(int, lines[1].split())
    return ro.join_list(ro.most_frequent_approx(s, k, d))

if __name__ == "__main__":
    print one_g('rosalind_1g_sample.dat')
    print one_g('rosalind_1g.dat')
