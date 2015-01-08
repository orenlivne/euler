'''
============================================================
http://rosalind.info/problems/itwv

Given three strings s, t, and u, we say that t and u can be
interwoven into s if there is some substring of s made up of
t and u as disjoint subsequences.

For example, the strings "ACAG" and "CCG" can be interwoven
into "GACCACGGTT". However, they cannot be interwoven into
"GACCACAAAAGGTT" because of the appearance of the four 'A's
in the middle of the subsequences. Similarly, even though
both "ACACG" is a shortest common supersequence of ACAG and
CCG, it is not possible to interweave these two strings into
"ACACG" because the two desired subsequences must be
disjoint; see "Interleaving Two Motifs" for details on
finding a shortest common supersequence of two strings.

Given: A text DNA string s of length at most 10 kbp,
followed by a collection of n (n<=10) DNA strings of length
at most 10 bp acting as patterns.

Return: An nxn matrix M for which Mjk=1 if the jth and kth
pattern strings can be interwoven into s and Mjk=0
otherwise.
============================================================
'''
import rosalind.rosutil as ro, rosalign as ra

def can_be_interwoven(s, t, u):
    '''Return True if and only if the motifs t and u can be interwoven into the string s.'''
    nt, nu = len(t), len(u)
    # Allocation + initial condition at i=0. First and last column correspond to the empty motifs.
    # At step i in the outer loop (x=s[i]), m[j,k] = (s[0..i] ENDS with an interweaving of
    # t[0..j], u[0..k] can be interwoven); m_old holds m[i-1, :, :]. 
    m, m_old = ro.zeros_bool_array(nt + 1, nu + 1), ro.zeros_bool_array(nt + 1, nu + 1)
    m[0][0] = -1;  # m_max = m[-1][-1]
    # Dynamic programming - prefixes of s
    for x in s:
        ra.copy_list(m, m_old)
        # Initial condition - first row (j=0)
        for k, uk in enumerate(u, 1):
            m[0][k] = m_old[0][k - 1] if x == uk else 0
        # Initial condition - first column (k=0)
        for j, tj in enumerate(t, 1):
            m[j][0] = m_old[j - 1][0] if x == tj else 0
            # Dynamic programming - prefixes of t,u in s[0..i] vs. in s[0..i-1].
            for j, tj in enumerate(t, 1):
                for k, uk in enumerate(u, 1):
                    mjk = 0
                    if x == tj: mjk |= m_old[j - 1][ k]
                    if x == uk: mjk |= m_old[j][k - 1]
                    m[j][k] = mjk
        # Shortcut: since it's a boolean result and we are OR-ing, once it's True it
        # must stay True, so no need to complete the entire outer loop over s. Had we
        # needed an integer result, we'd have to do the maximization over all s prefixes
        if m[-1][-1]: return True
        #m_max |= m[-1][-1]
    #return m_max
    return False
    
def itwv_matrix(s, t):
    '''Return the boolean matrix M.'''
    # By symmetry, we only need to call can_be_interwoven() for M's upper triangular part
    n = len(t)
    m = ro.zeros_bool_array(n, n)
    for i, ti in enumerate(t):
        for j in xrange(i, n):
            m[i][j] = can_be_interwoven(s, ti, t[j])
            m[j][i] = m[i][j]
    return m
    
def itwv(f):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    m = itwv_matrix(lines[0], lines[1:])
    for j in xrange(len(m)): print ' '.join('%d' % (m[j][k],) for k in xrange(len(m[j])))

if __name__ == "__main__":
    itwv('rosalind_itwv_sample.dat')
    itwv('rosalind_itwv.dat')
