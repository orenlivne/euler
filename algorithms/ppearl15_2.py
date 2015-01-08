'''
============================================================
Find the longest repeated phrase in a string. 
============================================================
'''
def lcs(s, i, j):
    '''Return the longest common substring length in s[i:], s[j:].'''
    k, max_k = 0, len(s) - max(i, j)
    while k < max_k and s[i + k] == s[j + k]: k += 1
    return k

def lrs(s, debug=False):
    '''Return the longest repeated substring of s.'''
    n = len(s)
    if n == 1: return ''  # One-character string, no non-trivial repeated substring exists
    
    # Build suffix array
    def compare_suffixes(i, j):
        if i == j: return 0
        k = lcs(s, i, j)
        max_k = n - max(i, j)
        if k == max_k: return -1 if i > j else 1  # Both substrings equal to end of string but the one with the largest index is shorter
        else: return -1 if s[i + k] < s[j + k] else 1  # Unequal at a character before end of string
    
    suffix = sorted(xrange(n), cmp=compare_suffixes)
    
    if debug:
        print 's = \'%s\'' % (s,)
        for i, p  in enumerate(suffix):
            print '%2d \'%s\'' % (i, s[p:]),
            if i < n - 1:
                k = lcs(s, p, suffix[i + 1]) 
                print 'LCS=%d \'%s\'' % (k, s[p:p + k]),
            print ''
    
    # Find max LCS of adjacent elements in suffix array
    k, i = max((lcs(s, suffix[i], suffix[i + 1]), suffix[i]) for i in xrange(n - 1))
    return s[i:i + k]

if __name__ == "__main__":
    print lrs('banana')  # ana
    print lrs('acgtacgt')  # acgt
    print lrs('Ask not what your country can do for you, but what you can do for your country')  # acgt
