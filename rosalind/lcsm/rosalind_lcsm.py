'''
============================================================
http://rosalind.info/problems/lcsm

Given: A collection of k (k <= 100) DNA strings of length at most 1 kbp each in FASTA format.

Return: A longest common substring of the collection. (If multiple solutions exist, you may return any single solution.)
============================================================
'''
from rosalind.rosutil import fafsa_itervalues

def is_subs(s, t):
    '''Is t a subsequence of s?'''
    n, t0, last = len(t), t[0], len(s) - len(t)
    return any(s[j:j + n] == t for j in (j for (j, sj) in enumerate(s) if j <= last and sj == t0))

'''All length-n subsequences of s.'''
all_subs = lambda s, n: [s[j:j + n] for j in xrange(0, len(s) - n + 1)]

def _lcsm_pair(s1, s2):
    '''Return the set of longest subsequences of s2 that are also substrings of s1.'''
    check = lambda t: is_subs(s1, t)
    # for m in xrange(len(s2), 0, -1): # too expensive
    print '_lcsm_pair()'
    print s1
    print s2
    T_old = set([])
    for m in xrange(1, len(s2) + 1):
        T = set(filter(check, all_subs(s2, m)))
        print 'm', m, '|T|', len(T)#, 'T', T
        if not T:
            return T_old
        T_old = T
    return T_old

'''Step 1: return a set of all longest subsequences common to s1,s2.'''
lcsm_pair = lambda s1, s2: _lcsm_pair(s1, s2) if len(s2) < len(s1) else _lcsm_pair(s2, s1)
    
def trim_subs_set(s, T):
    '''Given a set of equal-length sequences t, return a set T' of all longest sequences 
    that are also common to s. Each element of T' is a subsequence of an element of T.'''
    if not T: return T
    m = len(iter(T).next())
    while m > 0:
        T_found = set(filter(lambda t: is_subs(s, t), T))
        if T_found: return T_found  # Found one or more longest sub-sequences, no need to go shorter
        m -= 1  # Trim T to the list of candidates of one-shorter-length and retry fitting them into s
        if m > 0:
            T = set(sum((all_subs(t, m) for t in T), []))
    return set([])  # no common subsequences

def lcsm(S):
    '''Longest Common substring of a string collection S. |S| >= 2.'''
#     S = list(S)
#     print 'lcsm()', '|S|', len(S)
#     for s in S:
#         print s
    it = iter(S)
    T = lcsm_pair(it.next(), it.next())
    count = 2
    # print '#strings', count, 'T', T
    if not T: return T
    while True:  # Step 2: dynamic programming
        try:
            T = trim_subs_set(it.next(), T)
            count += 1
            # print '#strings', count, 'T', T
            if not T: return T
        except StopIteration:
            break
    return T

def solve_lcsm(file_name):
    '''Solve the LCSM problem.'''
    T = lcsm(fafsa_itervalues(file_name))
    return iter(T).next() if T else ''

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    from numpy.ma.testutils import assert_equal
    assert_equal(lcsm_pair('TCGGTTCGCACCATG', 'CACCA'), set(['CACCA']))
    assert_equal(lcsm_pair('TCGGTTCGCACCA',
                            'TTCCCACACCA'),
                 set(['CACCA']))

    assert_equal(lcsm_pair('GATTACA', 'TAGACCA'), set(['GA', 'AC', 'CA', 'TA']))
    assert_equal(lcsm_pair('AACC', 'CCAA'), set(['AA', 'CC']))
    assert_equal(lcsm_pair('TCGGTTCGCACCATGGTACACTAGGTACAGATAAGCCGTTTCATGGATTTTGCGTTGATT',
                            'CGGAATTCGGCACGTAATTATACCATTCCCAATCACCACAGCGGCTCCTTCCACCAAGCG'),
                 set(['CACCA', 'ACCAT']))
    assert_equal(lcsm_pair('CACCA', 'TCGGTTCGCACCATG'), set(['CACCA']))

    assert_equal(lcsm(['ACAC', 'CACA', 'ACA']), set(['ACA']))

#     print solve_lcsm('rosalind_lcsm_sample.dat')
#     print solve_lcsm('rosalind_lcsm1.dat')
#     print solve_lcsm('rosalind_lcsm2.dat')
    print solve_lcsm('rosalind_lcsm3.dat')
