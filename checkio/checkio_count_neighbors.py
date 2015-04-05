def count_neighbours(grid, row, col):
    m, n = len(grid), len(grid[0])
    padded = [[0 for _ in xrange(n+2)] for _ in xrange(m+2)]
    for i in xrange(1,m+1):
        for j in xrange(1,n+1):
            padded[i][j] = grid[i-1][j-1]
            return sum(padded[i][j] fori in xrange(row,row+3) for j in xrange(col,col+3)) - padded[row+1][col+1]


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert count_neighbours(
        ((1, 0, 0, 1, 0),
         (0, 1, 0, 0, 0),
         (0, 0, 1, 0, 1),
         (1, 0, 0, 0, 0),
         (0, 0, 1, 0, 0),), 1, 2) == 3, "1st example"
    assert count_neighbours(((1, 0, 0, 1, 0),
                             (0, 1, 0, 0, 0),
                             (0, 0, 1, 0, 1),
                             (1, 0, 0, 0, 0),
                             (0, 0, 1, 0, 0),), 0, 0) == 1, "2nd example"
    assert count_neighbours(((1, 1, 1),
                             (1, 1, 1),
                             (1, 1, 1),), 0, 2) == 3, "Dense corner"
    assert count_neighbours(((0, 0, 0),
                             (0, 1, 0),
                             (0, 0, 0),), 1, 1) == 0, "Single"
