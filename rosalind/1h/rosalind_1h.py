'''
============================================================
http://rosalind.info/problems/1h

Find the most frequent k-mers (with mismatches and reverse complements) in a DNA string.

Given: A DNA string Text as well as integers k and d.

Return: All k-mers Pattern maximizing the sum Countd(Text, Pattern) + Countd(Text, Pattern) over all possible k-mers.
============================================================
'''
import rosalind.rosutil as ro
from collections import Counter

def one_h(f):
    '''Main driver for solving this problem.'''
    lines = ro.read_lines(f)
    s, (k, d) = lines[0], map(int, lines[1].split())
    c = ro.possible_kmers_counter(s, k, d)
    return ro.join_list(ro.most_frequent(c + Counter(dict((ro.revc(x), v) for x, v in c.iteritems()))))

if __name__ == "__main__":
    print one_h('rosalind_1h_sample.dat')
    print one_h('rosalind_1h.dat')
    
