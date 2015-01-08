'''
============================================================
http://rosalind.info/problems/1c

Find the most frequent k-mers in a string.

Given: A string Text and an integer k.

Return: All most frequent k-mers in Text.
============================================================
'''
import rosalind.rosutil as ro

def one_c(f):
    pattern, text = ro.read_lines(f)
    return ' '.join(map(str, ro.find_all(text, pattern)))

if __name__ == "__main__":
    print one_c('rosalind_1c_sample.dat')
    print one_c('rosalind_1c.dat')
    