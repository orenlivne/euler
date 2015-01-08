'''
============================================================
http://rosalind.info/problems/revp

A DNA string is a reverse palindrome if it is equal to its reverse complement. For instance, GCATGC is a reverse palindrome because its reverse complement is GCATGC. See Figure 2.

Given: A DNA string of length at most 1 kbp in FASTA format.

Return: The position and length of every reverse palindrome in the string having length between 4 and 12. You may return these pairs in any order.
============================================================
'''
from rosalind.rosutil import COMPLEMENT, fafsa_itervalues
from itertools import dropwhile

def max_palindrome_length(s, i, max_len):
    '''Given a palindrome's center position i (between i and i+1 in python string character coordinates),
    output the length of the longest palindrome centered at i.'''
    j_max = min([i + 2, len(s) - i, max_len / 2 + 1])
    try: return 2 * (dropwhile(lambda j: s[i + j] == COMPLEMENT[s[i - j + 1]], xrange(1, j_max)).next() - 1)
    except StopIteration: return 2 * (j_max - 1)

def palindromes(s, min_len, max_len):
    '''Yield all palindrome 1-based start positions and lengths in the string s.'''
    for i in xrange(len(s)):
        j = max_palindrome_length(s, i, max_len)
        if j >= min_len:
            for k in xrange(j / 2, min_len / 2 - 1, -1):  yield i + 2 - k, 2 * k

def revp(file_name, min_len, max_len):
    print '\n'.join(' '.join(map(str, x)) for x in palindromes(fafsa_itervalues(file_name).next(), min_len, max_len))        
        
if __name__ == "__main__":
    #revp('rosalind_revp_sample.dat', 4, 12)
    #revp('rosalind_revp_sample2.dat', 2, 12)
    revp('rosalind_revp.dat', 4, 12)
    
