'''
============================================================
http://rosalind.info/problems/qrtd

Given: A list containing n taxa (n<=2000) and two unrooted
binary trees T1 and T2 on the given taxa. Both T1 and T2 are
given in Newick format.

Return: The quartet distance dq(T1,T2).
============================================================
'''

# Broken even for the sample problem; finally solved using the QDist software http://birc.au.dk/software/qdist/

import rosalind.rosutil as ro, itertools as it, numpy as np

leaves = lambda t: t.translate(None, '();').split(',')

def dq(t1, t2):
    s = map(dict((v, k) for k, v in enumerate(leaves(t1))).__getitem__, leaves(t2))
    n, d = len(s), 0
    p, q = np.arange(n), np.arange(n - 1, -1, -1)  # p[k] = #(elements in s[j+1:n] < k); q[k] = #(elements in s[j+1:n] > k)
    # print 's', s
    # print 'p', p, 'q', q
    print 'n', n 
    for j, y in enumerate(s):
        print 'j', j
        p[y + 1:] -= 1
        q[:y] -= 1 
        # print 'j', j, 'y', y, 's[%d:]' % (j,), s[j + 1:], 'p', p, 'q', q
        for x in it.islice(s, j):
            a, b = (p[x], q[y]) if x < y else (p[y], q[x])
            # print (x, y), 'a', a, 'b', b, 'options', (a - 1) * a / 2, b * (b - 1) / 2
            d += a * (a - 1) + b * (b - 1)
    # print 'q(T1)', n * (n - 1) * (n - 2) * (n - 3) / 24, 'q(T1,T2)', d / 2
    return n * (n - 1) * (n - 2) * (n - 3) / 12 - d

def qrtd(f):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    return dq(lines[1], lines[2])

if __name__ == "__main__":
    print qrtd('rosalind_qrtd_sample.dat')
    #print qrtd('rosalind_qrtd.dat')
