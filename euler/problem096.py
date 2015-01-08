'''
============================================================
http://projecteuler.net/problem=96

Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.

0 0 3
9 0 0
0 0 1    0 2 0
3 0 5
8 0 6    6 0 0
0 0 1
4 0 0
0 0 8
7 0 0
0 0 6    1 0 2
0 0 0
7 0 8    9 0 0
0 0 8
2 0 0
0 0 2
8 0 0
0 0 5    6 0 9
2 0 3
0 1 0    5 0 0
0 0 9
3 0 0

4 8 3
9 6 7
2 5 1    9 2 1
3 4 5
8 7 6    6 5 7
8 2 1
4 9 3
5 4 8
7 2 9
1 3 6    1 3 2
5 6 4
7 9 8    9 7 6
1 3 8
2 4 5
3 7 2
8 1 4
6 9 5    6 8 9
2 5 3
4 1 7    5 1 4
7 6 9
3 8 2
A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.

The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.
============================================================
'''
import numpy as np, itertools as it

DIGIT_SET = set(range(1, 10))

class Position(object):
    def __init__(self, grid, var=None, title=None):
        self.grid = grid
        self.vars = var if var is not None else \
        dict((z, DIGIT_SET - set(grid[Position.to_ind(self.all_nbhrs(z))])) 
             for z in it.izip(*np.where(grid == 0)))
        self.title = title
    
    @staticmethod
    def to_ind(s): return tuple(it.izip(*s))
    def __repr__(self): return self.title + '\n' + str(self.grid)
    def copy(self): return Position(self.grid.copy(), var=dict((k, v.copy()) for k, v in self.vars.iteritems()), title=self.title)
    def row_of(self, (i, j)): return ((i, j) for j in xrange(9))
    def col_of(self, (i, j)): return ((i, j) for i in xrange(9))
    def cell_of(self, (i, j)):
        s, t = 3 * (i / 3), 3 * (j / 3)
        return it.product(xrange(s, s + 3), xrange(t, t + 3))
    def all_nbhrs(self, y): return (z for z in it.chain(self.row_of(y), self.col_of(y), self.cell_of(y)) if z != y)  # Does not include (i,j)
    def var_nbhrs(self, y): return (z for z in self.all_nbhrs(y) if self.grid[z] == 0)
    
    def set_var(self, (i, j), v):
        self.grid[i, j] = v
        del self.vars[(i, j)]
    
    def min_var_nbhrs(self, z): return min(self.__num_vars(z, self.row_of(z)), self.__num_vars(z, self.col_of(z)), self.__num_vars(z, self.cell_of(z)))
    def __num_vars(self, y, s): return sum(1 for z in s if z != y and self.grid[z] == 0)

def set_var_deduction(position, y, v, count):
    '''Set location k to v in the Sudoku position ''position'' and carry out all possible deduction steps.'''
    #print count * '  ' + 'set (%d,%d) -> %d' % (y[0], y[1], v)
    position.set_var(y, v)
    if not position.vars: return position  # Found solution
    
    N, D = position.var_nbhrs(y), []  # N = y's neighboring zeroes; D = newly determined zeroes after y is set to v
    #print count * '  ' + 'N = %s' % (repr(list(position.var_nbhrs(y))),)
    count += 1
    for z in N:
        values = position.vars[z]
        values.discard(v)
        if not values:
            #print count * '  ' + 'Illegal position: (%d,%d) has no values' % z  
            return None  # No permissible values for z ==> illegal position reached      
        elif len(values) == 1: D.append((z, iter(values).next()))  # z is now determined to the single value in the values set
    
    for z, vz in D:  # Recursively deduce
        if position.grid[z] == 0:  # If z still hasn't been determined by previous iterations of this loop, set its value to vz
            position = set_var_deduction(position, z, vz, count)
            if not position: return None  # Illegal position reached during recursion
            elif not position.vars: return position  # Found solution during recursion
    
    return position

valid_set = lambda s: set(s) == DIGIT_SET
valid_solution = lambda g: all(valid_set(g[i, :]) for i in xrange(9)) & all(valid_set(g[:, j]) for j in xrange(9)) & all(valid_set(g[s:s + 3, t:t + 3].flatten()) for t in xrange(0, 9, 3) for s in xrange(0, 9, 3))

def sudoku_solve((grid, title)):
    p = Position(grid, title=title)
    #print p
    q = _solve(p)
    if not valid_solution(q.grid): 
        #print q
        raise ValueError('Invalid solution')
    #print q
    #print grid_code(q.grid)
    #print '-' * 70
    return q.grid

def _solve(position, count=0):
    if not position.vars: return position
    z = min((position.min_var_nbhrs(z), z) for z in position.vars.iterkeys())[1]
    #print count * '  ' + 'z = (%d,%d), possible values %s' % (z[0], z[1], repr(position.vars[z]))
    count += 1
    for v in position.vars[z]:
        #print count * '  ' + 'Search branch: set (%d,%d) -> %d' % (z[0], z[1], v)
        p = set_var_deduction(position.copy(), z, v, count)
        if not p: pass
        elif not p.vars: return p
        else:
            q = _solve(p, count + 1)
            if q: return q
    return None  # No solution found in all search branches

def read_grids(file_name):
    z = ord('0')
    with open(file_name, 'rb') as f:
        try:
            while True:
                title = f.next().rstrip('\r\n').rstrip('\n')  # Header line
                yield (np.concatenate(list(np.fromstring(f.next().rstrip('\r\n').rstrip('\n'), dtype=np.byte)[np.newaxis] - z for _ in xrange(9)), axis=0), title)
        except StopIteration: return  # EOF
        
grid_code = lambda grid: 100 * grid[0, 0] + 10 * grid[0, 1] + grid[0, 2]

if __name__ == "__main__":
    print sum(map(grid_code, it.imap(sudoku_solve, read_grids('problem096.dat'))))
