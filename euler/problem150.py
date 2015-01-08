'''
============================================================
http://projecteuler.net/problem=150

In a triangular array of positive and negative integers, we wish to find a sub-triangle such that the sum of the numbers it contains is the smallest possible.

In the example below, it can be easily verified that the marked triangle satisfies this condition having a sum of -42.


We wish to make such a triangular array with one thousand rows, so we generate 500500 pseudo-random numbers sk in the range +-219, using a type of random number generator (known as a Linear Congruential Generator) as follows:

t := 0 
for k = 1 up to k = 500500: 
    t := (615949*t + 797807) modulo 220 
    sk := t-219

Thus: s1 = 273519, s2 = -153582, s3 = 450905 etc

Our triangular array is then formed using the pseudo-random numbers thus:

s1 
s2  s3 
s4  s5  s6  
s7  s8  s9  s10 
...
Sub-triangles can start at any element of the array and extend down as far as we like (taking-in the two elements directly below it from the next row, the three elements directly below from the row after that, and so on). 
The "sum of a sub-triangle" is defined as the sum of all the elements it contains. 
Find the smallest possible sub-triangle sum.

============================================================
'''
from numpy import cumsum

OFFSET = 2 ** 19
MODULUS = 2 * OFFSET

def lc_generator(t):
    '''Linear Congruence (LC) generator. Given a seed, returns the new seed and a random value.'''
    t = (615949 * t + 797807) % MODULUS
    return t, t - OFFSET

def triangle_data(N, gen, t):
    '''Generate an N-row triangle using the random generator functor gen with an initial seed value
    t. The triangle is represented by a list of N lists, where list i is of size i+1.'''
    a, i, j = [None] * N, -1, 0
    for _ in xrange(N * (N + 1) / 2):
        t, s = gen(t)
        if j > i:  # Allocate and advance pointer to a new triangle row
            i += 1
            j = 0
            a[i] = [None] * (i + 1)
            a_row = a[i]
        a_row[j] = s
        j += 1
    return a

def min_sub_triangle_sum(a):
    '''Return the minimum sub-triangle sum in the triangle a.'''
    b, N = min_rooted_sum(a), len(a)
    for i in xrange(N - 2, -1, -1):  # Implicit initial condition: Delta[N-1,:]=b[N-1,:] where Delta[i,j] = min sub-triangle sum within the sub-triangle rooted at (i,j)
        for j in xrange(i + 1):
            b[i][j] = min(b[i + 1][j], b[i + 1][j + 1], b[i][j])  # Dynamic programming: Delta (set into the b-array to reuse space) is the minimum of all sub-triangles rooted at (i,j) and all sub-triangles rooted below (i,j), i.e., at either (i+1,j) or (i+1,j+1). At this point, b-row number i+1 already contains delta values.
    # The solution is the minimum Delta over all possible (i,j)
    return min(x for b_row in b for x in b_row)

def min_rooted_sum(a):
    '''Return a new triangle b of the same size as the triangle a, where b[i][j] is the minimum
    sum of all sub-triangles rooted at (i,j).'''
    b, N = [None] * len(a), len(a)
    b[N - 1] = [None] * (N)
    for j in xrange(N): b[N - 1][j] = [a[N - 1][j]]  # Initial condition
    for i in xrange(N - 2, -2, -1):
        # For each row i and column j, calculate the list b[i][j] of line sums below (i,j).
        if i >= 0:
            b[i] = [None] * (i + 1)
            for j in xrange(i + 1):
                b_down = b[i + 1][j]
                b[i][j] = [a[i][j]] + [b_down[k] + a[i + 1 + k][j + 1 + k] for k in xrange(len(b_down))]
        # Now that row i is calculated based on i+1, replace b[i+1] with the min cumulative sum
        # of the line lists, which is the desired min sub-triangle sum rooted at (i,j).
        b_row_down = b[i + 1]
        for j in xrange(i + 2): b_row_down[j] = min(cumsum(b_row_down[j]))
    return b
                                      
if __name__ == "__main__":
    a = [[15], [-14, -7], [20, -13, -5], [-3, 8, 23, -26], [1, -4, -5, -18, 5], [-16, 31, 2, 9, 28, 3]]
    print min_sub_triangle_sum(a) # -42
    print min_sub_triangle_sum(triangle_data(1000, lc_generator, 0))
