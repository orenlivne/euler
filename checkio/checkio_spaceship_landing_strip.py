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
@author: Oren Livne <oren.livne@gmail.com>
============================================================
'''
import time, random, itertools as it

def log_two_int_value(x):
  return it.dropwhile(lambda k: (1 << k) <= x, xrange(x + 1)).next() - 1

def preprocess_rmq(a):
  # Returns a preprocessing Range Minimum Query (RMQ) array m for the array a.
  # m[j][i] = argmin(a[i:i+2**j+1]), i=0..n-1, j=0..[log(n)]-1.
  # https://www.topcoder.com/community/data-science/data-science-tutorials/range-minimum-query-and-lowest-common-ancestor/
  # Initialize m for the intervals of length 1.
  n = len(a)
  m = [range(n)]
  # Build m-values from smaller to bigger intervals.
  for j in it.count(1):
    power_two_j = 1 << j
    if power_two_j > n: break
    power_two_j_m1 = 1 << (j - 1)
    m_prev = m[j - 1]
    m.append([m_prev[i] if a[m_prev[i]] < a[m_prev[i + power_two_j_m1]]
              else m_prev[i + power_two_j_m1]
              for i in xrange(n + 1 - power_two_j)])
  return m

def range_minimum_query(a, m, i, j):
  # Returns the index of the minimum a[i:j+1].
  k = log_two_int_value(j - i + 1) # [log2(j-i+1)]
  power_two_k = 1 << k;
  return m[k][i if a[m[k][i]] <= a[m[k][j - power_two_k + 1]] else j - power_two_k + 1]

def print_matrix(a):
  m, n = len(a), len(a[0])
  for i in xrange(m):
    for j in xrange(n): print '%s\t' % (repr(a[i][j])),
    print ''

def transpose(a):
  # Returns the transpose of the matrix a.
  return [[a[i][j] for i in xrange(len(a))] for j in xrange(len(a[0]))]

def sub_array(a, i, k, j, l):
  # Returns the sub-array a[i:k,j:l].
  print 'sub_array(%d-%d, %d-%d)' % (i, k, j, l)
  return [[a[p][q] for q in xrange(j, l)] for p in xrange(i, k)]

def nearest_one_left_index(row, middle):
  # Returns the distance of the nearest one on the left of the index middle
  # in the boolean array row. Searches from middle - 1 downward; e.g., if
  # row[middle - 1] = 1, returns 1, and so on.
  n = len(row)
  try: i = it.dropwhile(lambda x: not x, xrange(middle - 1, -1, -1)).next()
  except StopIteration: i = 0
  return middle - i

def nearest_one_right_index(row, middle):
  # Returns the distance of the nearest one on the right of the index middle
  # in the boolean array row. Searches from middle upward; e.g., if
  # row[middle] = 1, returns 0, and so on.
  n = len(row) 
  try: i = it.dropwhile(lambda x: not x, xrange(middle, n)).next()
  except StopIteration: i = n - 1
  return i - middle

def max_rectangle_area_brute_force(a):
  # Returns the maximum area of a sub-matrix of a boolean matrix a that contains
  # only True values. O(N^2) brute-force solution where N = #cells in a.'''

  # TODO: replace all(.) clause by a dynamic programming that updates the number
  # of non-zeros by fixing the rectangle size and moving its starting position
  # one cell at a time and updating the number of non-zeros within it. As
  # implemented here, the method may take more than O(N^2). I wonder why we
  # still observe O(N^2) for random matrices.
  return max(k * l for i in xrange(len(a)) for j in xrange(len(a[0]))
             for k in xrange(1, len(a) - i + 1) for l in xrange(1, len(a[0]) - j + 1)
             if all(a[m][n] for m in xrange(i, i + k) for n in xrange(j, j + l)))

def max_rectangle_area_dc(a, max_brute_force_size=4):
  # Returns the maximum area of a sub-matrix of a boolean matrix a that contains
  # only True values. ~O(N log N) divide-and-conquer implementation where
  # N = #cells in a.
  # If matrix is small enough, use brute-force. max_brute_force_size is a tunable parameter.
  m, n = len(a), len(a[0])
  if min(m, n) == 1 or m * n <= max_brute_force_size: return max_rectangle_area_brute_force(a)

  # Reduce to a matrix with m <= n.
  if m > n:
    a = transpose(a)
    m, n = n, m

  print 'dc(%d x %d)' % (m, n)

  # Conquer step: rectangle straddles the middle column i = m/2.
  middle = m/2
  # For every row, find the distance of the nearest one on the left of the
  # middle line from the middle line.
  left = [nearest_one_left_index(row, middle) for row in a]
  # For every row, find the distance of the nearest one on the right of the
  # middle line from the middle line.
  right = [nearest_one_right_index(row, middle) for row in a]
  # Build a data structure that allows us to query the maximum rectangle width
  # between each two heights start, stop along the middle column.
  m_left = preprocess_rmq(left)
  m_right = preprocess_rmq(right)
  # For each two heights, find the maximum 1-rectangle width to the left and to
  # the right of the middle. This rectangle ranges from min(left[start:stop+1])
  # distance to the left the middle to min(right[start:stop+1]) to the right of
  # the boundary
#  print 'left', left
#  print 'm_left', m_left
#  i, j = 0, 4
#  print i, j
#  actual, expected = left[range_minimum_query(left, m_left, i, j)], min(a[i:j+1])

  for start in xrange(m):
    for stop in xrange(start, m):
#      print start, stop
#      print range_minimum_query(left, m_left, start, stop)
#      print range_minimum_query(right, m_right, start, stop)
#  max_straddling_rectangle_area = max((stop - start + 1) * (range_minimum_query(left, m_left, start, stop) + range_minimum_query(right, m_right, start, stop)) for start in xrange(m) for stop in xrange(start, m))
      max_straddling_rectangle_area = \
      max((stop - start + 1) * 
          (min(left[start:stop+1]) + min(right[start:stop+1]))
          for start in xrange(m) for stop in xrange(start, m))

  # Divide step: max rectangle is either in the left half, in the right half, or
  # straddles the middle column.
  return max(max_rectangle_area_dc(sub_array(a, 0, middle, 0, n)),
             max_rectangle_area_dc(sub_array(a, middle, m, 0, n)),
             max_straddling_rectangle_area)

def checkio(landing_map):
    a = [[x in 'GS' for x in row] for row in landing_map]
    print '-' * 80
    print_matrix(a)
    return max_rectangle_area_dc(a)

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
        if not all(x == result[0] for x in result):
          raise ValueError('Different methods gave different results')
      t = [x / num_experiments for x in t] 
      print '%3d x %3d = %6d cells' % (m, n, m * n),
      for i in xrange(num_methods):
        print '\t%s: %.2f sec [%.2f]' % (methods[i][0], t[i], t[i] / t_old[i] if k > 0 else 0),
      print ''
      sz *= 2

def max_rectangle_area_dp(a):
  # Dynamic programming solution from http://stackoverflow.com/questions/11481868/largest-rectangle-of-1s-in-2d-binary-matrix. O(N).
  # Similar to my divide-and-conquer, but no need for divide-and-conquer here. So no log term. Oh well. :)
  m, n = len(a), len(a[0])

  h = [[0 for _ in xrange(n)] for _ in xrange(m)]
  for i in xrange(1, m):
    for j in xrange(1, n):
      h[i][j] = 0 if a[i][j] else (h[i-1][j] + 1)

  l = [[0 for _ in xrange(n)] for _ in xrange(m)]
  for j in xrange(1, n):
    for i in xrange(m):
      l[i][j] = c-p if a[i-1][j] == 0 else min(l[i-1][j], j - p)

  r = [[0 for _ in xrange(n+1)] for _ in xrange(m)]
  for j in xrange(n, -1, -1):
    for i in xrange(m):
      r[i][j] = p-c if a[i-1][j] == 0 else min(r[i - 1][j], p - c)

# where p is the column of the previous 0 as we populate l from left-right and r from right-left.
  return max((h[i][j] * (l[i][j] + r[i][j] - 1)) for i in xrange(len(a)) for j in xrange(len(a[0]))


def test_rmq(a):
  # Test range minium query module vs. brute force for all possible sub-arrays
  # of the array a.
  m = preprocess_rmq(a)
  for i in xrange(len(a)):
    for j in xrange(i, len(a)):
      actual, expected = a[range_minimum_query(a, m, i, j)], min(a[i:j+1])
      assert actual == expected

if __name__ == '__main__':
  test_rmq([8, 7, 3, 20, 2, 17, 5, 21, 11, 12])

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
                ('Dynamic programming', max_rectangle_area_dc)],
                num_experiments=10)
