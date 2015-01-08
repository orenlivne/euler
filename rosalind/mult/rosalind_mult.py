'''
============================================================
http://rosalind.info/problems/mult

A multiple alignment of a collection of three or more strings is formed by adding gap symbols to the strings to produce a collection of augmented strings all having the same length.

A multiple alignment score is obtained by taking the sum of an alignment score over all possible pairs of augmented strings. The only difference in scoring the alignment of two strings is that two gap symbols may be aligned for a given pair (requiring us to specify a score for matched gap symbols).

Given: A collection of four DNA strings of length at most 10 bp in FASTA format.

Return: A multiple alignment of the strings having maximum score, where we score matched symbols 0 (including matched gap symbols) and all mismatched symbols -1 (thus incorporating a linear gap penalty of 1).
============================================================
'''
import rosalind.rosutil as ro, numpy as np, rosalign as ra

def align3(s, score, gap_score= -1, debug=False):
    '''Alignment of three strings.'''
    x, y, z = s
    c = np.zeros(tuple(len(sp) + 1 for sp in s), dtype=object)
    
    #---------------------
    # Initial conditions
    #---------------------
    # Align pairs of strings
    c[0, :, :] = ra.global_alignment_matrix((s[1], s[2]), score=score, gap_score=gap_score, debug=debug)
    c[:, 0, :] = ra.global_alignment_matrix((s[0], s[2]), score=score, gap_score=gap_score, debug=debug)
    c[:, :, 0] = ra.global_alignment_matrix((s[0], s[1]), score=score, gap_score=gap_score, debug=debug)
    # Add gap penalty to each c-face
    for i in xrange(c.shape[1]):
        for j in xrange(1, c.shape[2]): c[0, i, j] = (c[0, i, j][0] + (i + j) * gap_score, (0, c[0, i, j][1][0], c[0, i, j][1][1]))
    for i in xrange(c.shape[2]):
        for j in xrange(1, c.shape[0]): c[j, 0, i] = (c[j, 0, i][0] + (i + j) * gap_score, (c[j, 0, i][1][0], 0, c[j, 0, i][1][1]))
    for i in xrange(c.shape[0]):
        for j in xrange(1, c.shape[1]): c[i, j, 0] = (c[i, j, 0][0] + (i + j) * gap_score, (c[i, j, 0][1][0], c[i, j, 0][1][1], 0))

    #---------------------
    # Dynamic programming
    #---------------------
    g2 = 2 * gap_score
    for i, xi in enumerate(x, 1):
        for j, yj in enumerate(y, 1):
            s_xy = score(xi, yj)
            for k, zk in enumerate(z, 1):
                s_xz, s_yz = score(xi, zk), score(yj, zk)
                c[i, j, k] = max((c[i - 1, j - 1, k - 1][0] + s_xy + s_xz + s_yz, (i - 1, j - 1, k - 1)),
                                 (c[i, j - 1, k - 1][0] + s_yz + g2, (i, j - 1, k - 1)),
                                 (c[i - 1, j, k - 1][0] + s_xz + g2, (i - 1, j, k - 1)),
                                 (c[i - 1, j - 1, k][0] + s_xy + g2, (i - 1, j - 1, k)),
                                 (c[i - 1, j, k][0] + g2, (i - 1, j, k)),
                                 (c[i, j - 1, k][0] + g2, (i, j - 1, k)),
                                 (c[i, j, k - 1][0] + g2, (i, j, k - 1)))
    return c

def alignment3((x, y, z), c, gap_symbol='-'):
    '''Return the augmented-aligned strings of the original strings x,y,z
    from the DP result c.'''
    s, t, u, i, j, k = '', '', '', len(x), len(y), len(z)
    # print i, j, k
    while i or j or k:
        ip, jp, kp = c[i, j, k][1]
        s, t, u = \
        (gap_symbol if ip == i else x[i - 1]) + s, \
        (gap_symbol if jp == j else y[j - 1]) + t, \
        (gap_symbol if kp == k else z[k - 1]) + u
        i, j, k = ip, jp, kp
        # print i, j, k
    return s, t, u

def align4(s, score, gap_score= -1, debug=False):
    '''Alignment of four strings.'''
    x, y, z, w = s
    c = np.zeros(tuple(len(sp) + 1 for sp in s), dtype=object)
    
    #---------------------
    # Initial conditions
    #---------------------
    # Align pairs of strings
    c[0, :, :, :] = align3((s[1], s[2], s[3]), score=score, gap_score=gap_score, debug=debug)
    c[:, 0, :, :] = align3((s[0], s[2], s[3]), score=score, gap_score=gap_score, debug=debug)
    c[:, :, 0, :] = align3((s[0], s[1], s[3]), score=score, gap_score=gap_score, debug=debug)
    c[:, :, :, 0] = align3((s[0], s[1], s[2]), score=score, gap_score=gap_score, debug=debug)
    # Add gap penalty to each c-face
    for i in xrange(c.shape[1]):
        for j in xrange(c.shape[2]): 
            for k in xrange(1, c.shape[3]):
                c[0, i, j, k] = (c[0, i, j, k][0] + (i + j + k) * gap_score,
                                 (0, c[0, i, j, k][1][0], c[0, i, j, k][1][1], c[0, i, j, k][1][2]))
    for i in xrange(c.shape[2]):
        for j in xrange(c.shape[3]): 
            for k in xrange(1, c.shape[0]):
                c[k, 0, i, j] = (c[k, 0, i, j][0] + (i + j + k) * gap_score,
                                 (c[k, 0, i, j][1][0], 0, c[k, 0, i, j][1][1], c[k, 0, i, j][1][2]))
    for i in xrange(c.shape[3]):
        for j in xrange(c.shape[0]):
            for k in xrange(1, c.shape[1]):
                c[j, k, 0, i] = (c[j, k, 0, i][0] + (i + j + k) * gap_score,
                                 (c[j, k, 0, i][1][0], c[j, k, 0, i][1][1], 0, c[j, k, 0, i][1][2]))
    for i in xrange(c.shape[0]):
        for j in xrange(c.shape[1]):
            for k in xrange(1, c.shape[2]):
                c[i, j, k, 0] = (c[i, j, k, 0][0] + (i + j + k) * gap_score,
                                 (c[i, j, k, 0][1][0], c[i, j, k, 0][1][1], c[i, j, k, 0][1][2], 0))
              
    #---------------------
    # Dynamic programming
    #---------------------
    g3 = 3 * gap_score
    g4 = 4 * gap_score
    for i, xi in enumerate(x, 1):
        for j, yj in enumerate(y, 1):
            s_xy = score(xi, yj)
            for k, zk in enumerate(z, 1):
                s_xz, s_yz = score(xi, zk), score(yj, zk)
                for l, wl in enumerate(w, 1):
                    s_xw, s_yw, s_zw = score(xi, wl), score(yj, wl), score(zk, wl)
                    c[i, j, k, l] = max((c[i - 1, j - 1, k - 1, l - 1][0] + s_xy + s_xz + s_yz + s_xw + s_yw + s_zw, (i - 1, j - 1, k - 1, l - 1)),
                                     
                                        (c[i, j - 1, k - 1, l - 1][0] + s_yz + s_yw + s_zw + g3, (i, j - 1, k - 1, l - 1)),
                                        (c[i - 1, j, k - 1, l - 1][0] + s_xz + s_xw + s_zw + g3, (i - 1, j, k - 1, l - 1)),
                                        (c[i - 1, j - 1, k, l - 1][0] + s_xy + s_xw + s_yw + g3, (i - 1, j - 1, k, l - 1)),
                                        (c[i - 1, j - 1, k - 1, l][0] + s_xy + s_xz + s_yz + g3, (i - 1, j - 1, k - 1, l)),
                                     
                                        (c[i, j, k - 1, l - 1][0] + s_zw + g4, (i, j, k - 1, l - 1)),
                                        (c[i, j - 1, k, l - 1][0] + s_yw + g4, (i, j - 1, k, l - 1)),
                                        (c[i, j - 1, k - 1, l][0] + s_yz + g4, (i, j - 1, k - 1, l)),
                                        (c[i - 1, j, k, l - 1][0] + s_xw + g4, (i - 1, j, k, l - 1)),
                                        (c[i - 1, j, k - 1, l][0] + s_xz + g4, (i - 1, j, k - 1, l)),
                                        (c[i - 1, j - 1, k, l][0] + s_xy + g4, (i - 1, j - 1, k, l)),
                                        
                                        (c[i - 1, j, k, l][0] + g3, (i - 1, j, k, l)),
                                        (c[i, j - 1, k, l][0] + g3, (i, j - 1, k, l)),
                                        (c[i, j, k - 1, l][0] + g3, (i, j, k - 1, l)),
                                        (c[i, j, k, l - 1][0] + g3, (i, j, k, l - 1)))
    return c

def alignment4((x, y, z, w), c, gap_symbol='-'):
    '''Return the augmented-aligned strings of the original strings x,y,z,w
    from the DP result c.'''
    s, t, u, v, i, j, k, l = '', '', '', '', len(x), len(y), len(z), len(w)
    # print i, j, k, l
    while i or j or k or l:
        ip, jp, kp, lp = c[i, j, k, l][1]
        s, t, u, v = \
        (gap_symbol if ip == i else x[i - 1]) + s, \
        (gap_symbol if jp == j else y[j - 1]) + t, \
        (gap_symbol if kp == k else z[k - 1]) + u, \
        (gap_symbol if lp == l else w[l - 1]) + v
        i, j, k, l = ip, jp, kp, lp
        # print i, j, k,l 
    return s, t, u, v

def test_align2(f, (i, j), match_score=0, mismatch_score= -1, gap_score= -1, debug=False):
    '''Two-string test.'''
    s = ro.fafsa_values(f)
    score = lambda x, y: match_score if x == y else mismatch_score
    print (s[i], s[j])
    c = ra.global_alignment_matrix((s[i], s[j]), score, gap_score=gap_score)
    # print c
    print ro.join_list([c[-1, -1][0]] + list(ra.alignment_from_matrix((s[i], s[j]), c)), delimiter='\n')

def test_align3(f, (i, j, k), match_score=0, mismatch_score= -1, gap_score= -1, debug=False):
    '''Three-string test.'''
    s = ro.fafsa_values(f)
    score = lambda x, y: match_score if x == y else mismatch_score
    print (s[i], s[j], s[k])
    c = align3((s[i], s[j], s[k]), score, gap_score=gap_score)
    # print c
    print ro.join_list([c[-1, -1, -1][0]] + list(alignment3((s[i], s[j], s[k]), c)), delimiter='\n')
    
def mult(f, match_score=0, mismatch_score= -1, gap_score= -1, debug=False):
    '''Main driver to solve this problem.'''
    s = ro.fafsa_values(f)
    score = lambda x, y: match_score if x == y else mismatch_score
    c = align4(s, score, gap_score=gap_score)
    # print c
    print ro.join_list([c[-1, -1, -1, -1][0]] + list(alignment4(s, c)), delimiter='\n')

if __name__ == "__main__":
    # test_align2('rosalind_mult_sample.dat', (0, 1))
    # test_align3('rosalind_mult_sample.dat', (0, 1, 2))
    mult('rosalind_mult_sample.dat')
    mult('rosalind_mult.dat')
