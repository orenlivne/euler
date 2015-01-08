'''
============================================================
http://projecteuler.net/problem=81

In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by only moving to the right and down, is indicated in bold red and is equal to 2427.

131    673    234    103    18
201    96    342    965    150
630    803    746    422    111
537    699    497    121    956
805    732    524    37    331

Find the minimal path sum, in matrix.txt (right click and 'Save Link/Target As...'), a 31K text file containing a 80 by 80 matrix, from the top left to the bottom right by only moving right and down.
============================================================
'''
'''Parse a matrix line from the input stream.'''
read_row = lambda line: map(int, line.split(','))

def min_path_sum(lines):
    '''Return the minimum path sum in an n x n matrix. Requires only 2*n storage - only the current
    row list and sum list corresponding to that row need to be stored, not all rows.''' 
    s = read_row(lines.next())              # Read row 0
    n = len(s)
    for j in xrange(1, n): s[j] += s[j - 1] # Initial condition for sums
    for _ in xrange(1, n):                  # Dynamic programming, row-by-row
        a = read_row(lines.next())
        s[0] += a[0]                        # Initial condition for the current row
        for j in xrange(1, n): s[j] = min(s[j - 1], s[j]) + a[j]
    return s[-1]                            # Last sum-list element corresponds to lower-right corner 

if __name__ == "__main__":
    print min_path_sum(open('problem081.dat', 'rb'))
