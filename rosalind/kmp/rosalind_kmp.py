'''
============================================================
http://rosalind.info/problems/kmp

A prefix of a length n string s is a substring s[1:j]; a suffix of s is a substring s[k:n].

The failure array of s is an array P of length n for which P[k] is the length of the longest substring s[j:k] that is equal to some prefix s[1:k-j+1], where j cannot equal 1 (otherwise, P[k] would always equal k). By convention, P[1]=0.

Given: A DNA string s (of length at most 100 kbp) in FASTA format.

Return: The failure array of s.
============================================================
'''
import rosalind.rosutil as ro

def failure_array(s):
    n = len(s)
    k, i, p = 2, 0, [0] * (n + 1)
    p[0] = -1
    print 'n', n
    while k <= n:
        print 'k', k, 'i', i, 's[k-1]', s[k - 1]
        if s[k - 1] == s[i]:
            print 'Extend match to', s[k - i - 1:k], s[:i + 1]
            i += 1
            p[k] = i
            k += 1
        else: 
            if i > 0:
                print 'Back-track i from', i, 'to', p[i], 'match', s[:p[i]]
                i = p[i]  # Back-track to previous possible match
            else:
                print 'At beginning'
                k += 1  # Beginning of string, p[k] already initialized to 0 above
    return p[1:]

kmp = lambda f: ' '.join(repr(x) for x in failure_array(ro.read_fafsa(f)))

if __name__ == "__main__":
#    print kmp('rosalind_kmp.dat')
    print kmp('rosalind_kmp_sample.dat')
    # open('rosalind_kmp.out', 'wb').write(kmp('rosalind_kmp.dat') + '\n')
    
