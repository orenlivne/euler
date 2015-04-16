'''
============================================================
The Robots have discovered a new island and accidentally crashed on it. To survive, they need to create the largest rectangular field possible to make a landing strip. While surveying the land, they encountered a number of obstacles which they marked on their map. Each square of the map is marked according to whether it contains grass (G), rock (R), water (W), shrubs (S), or trees (T). While the grass can be mowed and the shrubs can be dug from the ground, the water, rocks, and trees cannot be removed with the tools at their disposal. Given these obstacles, they need your help to determine the area of the largest possible rectangular field.
The island map is represented as a list of strings. Each string contains letter characters which indicate the conditions for each square of land (G, R, W, S, or T). The map is rectangular.
strip
Input: An island map as a list of strings.
Output: The maximum area of the largest possible rectangle that can be cleared as an integer.
Precondition:
0 < len(landing_map) < 10
all(0 < len(row) < 10 for row in landing_map)

Created on Apr 16, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import time, random

def print_matrix(a, fmt):
    m, n = len(a), len(a[0])
    for i in xrange(m):
        for j in xrange(n): print '%s\t' % (repr(a[i][j])),
        print ''

def max_rectangle_area_dynamic_programming(a):
    '''Returns the maximum area of a sub-matrix of a boolean matrix a that contains only True values.
    O(N) dynamic programming solution where N = #cells in a.'''
    m, n = len(a), len(a[0])
    # Construct a matrix L where L[i][j] is the size (in cells) of the maximum all-True sub-matrix of a
    # whose bottom-left corner is (i-1,j-1), i=1,...,m, j=1,...,n. i=0, j=0 are conveniently-added dummy
    # rows.
    L = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    print '-' * 80
    print 'a'
    print_matrix(a, '%d')    
    for i in xrange(1, m + 1):
        for j in xrange(1, n + 1):
            if a[i - 1][j - 1]:
                left = L[i][j - 1]
                up = L[i - 1][j]
                if up == 0 and left == 0: L[i][j] = (1, 1)
                elif up == 0: L[i][j] = (left[0] + 1, 1)
                elif left == 0: L[i][j] = (1, up[1] + 1)
                else: L[i][j] = (min(left[0] + 1, up[0]), min(left[1], up[1] + 1))
                print i - 1, j - 1, 'left', left, 'up', up, 'L', L[i][j]
            else: L[i][j] = 0
    print_matrix(L, '%s')
    print max(0 if l == 0 else l[0] * l[1] for row in L for l in row)
    return max(0 if l == 0 else l[0] * l[1] for row in L for l in row)
                                                          
def checkio(landing_map):
    a = [[x in 'GS' for x in row] for row in landing_map]
    print a
    return max_rectangle_area_dynamic_programming(a)

def max_rectangle_area_brute_force(a):
    '''Returns the maximum area of a sub-matrix of a boolean matrix a that contains only True values.
    O(N^2) brute-force solution where N = #cells in a.''' 
    return max(k * l for i in xrange(len(a)) for j in xrange(len(a[0]))
               for k in xrange(1, len(a) - i + 1) for l in xrange(1, len(a[0]) - j + 1)
               if all(a[m][n] for m in xrange(i, i + k) for n in xrange(j, j + l)))

def compare_times(methods, num_experiments=100):
    num_methods = len(methods)
    sz = 100
    t = [-1 for _ in xrange(num_methods)]
    result = [0 for _ in xrange(num_methods)]
    for k in xrange(10):
        n = sz / 10
        m = 10
        t_old = t
        t = [0 for _ in xrange(num_methods)]
        for _ in xrange(num_experiments):
            a = [[random.random() < 0.5 for _ in xrange(n)] for _ in xrange(m)]
            for i in xrange(num_methods):
                start = time.time()
                result[i] = methods[i][1](a)
                t[i] = time.time() - start
            if not all(x == result[0] for x in result): raise ValueError('Different methods gave different results')
        t = [x / num_experiments for x in t] 
        print '%3d x %3d = %6d cells' % (m, n, m * n),
        for i in xrange(num_methods):
            print '\t%s: %.2f sec [%.2f]' % (methods[i][0], t[i], t[i] / t_old[i] if k > 0 else 0),
        print ''
        sz *= 2

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio([u'G']) == 1, 'One cell - one variant'
    assert checkio([u'GS',
                    u'GS']) == 4, 'Four good cells'
    assert checkio([u'GT',
                    u'GG']) == 2, 'Four cells, but with a tree'
    assert checkio([u'GGTGG',
                    u'TGGGG',
                    u'GSSGT',
                    u'GGGGT',
                    u'GWGGG',
                    u'RGTRT',
                    u'RTGWT',
                    u'WTWGR']) == 9, 'Classic'
    compare_times([('Brute-force', max_rectangle_area_brute_force),
                   ('Dynamic programming', max_rectangle_area_dynamic_programming)],
                  num_experiments=10)
