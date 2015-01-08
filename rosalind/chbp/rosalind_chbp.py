'''
============================================================
http://rosalind.info/problems/chbp

Given: A list of n species (n<=80) and an n-column character table C in which the jth column denotes the jth species.

Return: An unrooted binary tree in Newick format that models C.
============================================================
'''
import rosalind.rosutil as ro, numpy as np
from collections import Counter

def to_newick_tree(c, s):
    t = np.zeros((s.shape[0],), dtype='S100000')
    t[:] = s[:]
    rows = np.arange(c.shape[0])
    while c.shape[1] > 3:
#         print '-' * 80
#         print rows.shape, c.shape, t.shape
#         print rows
#         print c
#         print t
        try: i, count = next((i, count)
                             for i, count in ((i, Counter(ci)) for i, ci in enumerate(c)) 
                             if min(count.itervalues()) == 2)
        except StopIteration: raise ValueError('Inconsistent character set')
        value = 0 if count[0] <= count[1] else 1
        u, v = np.where(c[i] == value)[0]
#         print i, value, (u, v), c[i], 't[u]', t[u], 't[v]', t[v], 'row', rows[i]
#         print c[:, u]
#         print c[:, v]
        if not all(c[:, u] == c[:, v]): raise ValueError('Inconsistent character set')
        t[u] = '(' + t[u] + ',' + t[v] + ')'
        t = np.delete(t, v)
        c = np.delete(c, v, 1)
        c = np.delete(c, i, 0)
        rows = np.delete(rows, i)
#     print '-' * 80
#     print rows
#     print c
#     print t
    return '(' + ','.join(t) + ');'

def chbp(f):
    '''Main driver to solve this problem.'''
    lines = ro.read_lines(f)
    s = np.array(lines[0].split())
    c = np.array([map(int, line) for line in lines[1:]])
    return to_newick_tree(c, s)

if __name__ == "__main__":
    print chbp('rosalind_chbp_sample.dat')
    # print chbp('rosalind_chbp.dat')
