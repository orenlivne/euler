'''
============================================================
http://rosalind.info/problems/lexf

Given: A collection of at most 10 symbols defining an ordered alphabet, and a positive integer n (n<=10).
Return: All strings of length n that can be formed from the alphabet, ordered lexicographically.
============================================================
'''
import rosalind.rosutil as ro, itertools as it

def lexf(f):
    lines = list(ro.read_lines(f))
    a, n = lines[0].split(), int(lines[1])
    return '\n'.join(''.join(x) for x in it.product(*(a for _ in xrange(n))))

if __name__ == "__main__":
#    print lexf('rosalind_lexf_sample.dat')
    print lexf('rosalind_lexf.dat')
    
