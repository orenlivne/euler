'''
============================================================
http://rosalind.info/problems/1a

Find the most frequent k-mers in a string.

Given: A string Text and an integer k.

Return: All most frequent k-mers in Text.
============================================================
'''
import rosalind.rosutil as ro

def one_a(f):
    lines = ro.read_lines(f)
    s, k = lines[0], int(lines[1])
    return ro.join_list(ro.most_frequent_kmers(s, k))

if __name__ == "__main__":
#    print one_a('rosalind_1a_sample.dat')
    print one_a('rosalind_1a.dat')
    
