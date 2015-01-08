'''
============================================================
http://projecteuler.net/problem=185

The game Number Mind is a variant of the well known game Master Mind.

Instead of coloured pegs, you have to guess a secret sequence of digits. After each guess you're only told in how many places you've guessed the correct digit. So, if the sequence was 1234 and you guessed 2036, you'd be told that you have one correct digit; however, you would NOT be told that you also have another digit in the wrong place.

For instance, given the following guesses for a 5-digit secret sequence,

90342 ;2 correct
70794 ;0 correct
39458 ;2 correct
34109 ;1 correct
51545 ;2 correct
12531 ;1 correct

The correct sequence 39542 is unique.

Based on the following guesses,

5616185650518293 ;2 correct
3847439647293047 ;1 correct
5855462940810587 ;3 correct
9742855507068353 ;3 correct
4296849643607543 ;3 correct
3174248439465858 ;1 correct
4513559094146117 ;2 correct
7890971548908067 ;3 correct
8157356344118483 ;1 correct
2615250744386899 ;2 correct
8690095851526254 ;3 correct
6375711915077050 ;1 correct
6913859173121360 ;1 correct
6442889055042768 ;2 correct
2321386104303845 ;0 correct
2326509471271448 ;2 correct
5251583379644322 ;2 correct
1748270476758276 ;3 correct
4895722652190306 ;1 correct
3041631117224635 ;3 correct
1841236454324589 ;3 correct
2659862637316867 ;2 correct

Find the unique 16-digit secret sequence.
============================================================
'''
import numpy as np # Requires numpy 1.7.1+
from itertools import combinations

'''Value of a guess entry known to be either correct or wrong.'''
X = np.byte(-1)

class Position(object):
    '''Holds the current position: guesses, correct elemenst and the constructed secret sequence.''' 
    def __init__(self, guess, correct, seq, depth=0, remove_zero_rows=True, wrong=None):
        self.depth = depth
        self.indent = self.depth * '  ' 

        self.guess = guess
        self.correct = correct
        self.seq = seq
        # Number of digits with unknown status (neither correct nor incorrect) in each guess
        self.left = np.sum(self.guess != X, 1)
        self.wrong = wrong if wrong else [set() for _ in xrange(self.n)]
        if remove_zero_rows: self.remove_zero_rows()

    def __repr__(self):
        s = ''
        g = self.guess
        s += self.indent + ' '.join(map(lambda x: '-' if x < 0 else '%d' % (x,), self.seq)) + ' (%2d)' % (self.num_seq_filled,) + '\n'
        s += self.indent + '-' * (self.n * 3 + 7) + '\n'
        for i in xrange(self.m):
            s += self.indent + ' '.join(map(lambda x: '-' if x < 0 else '%d' % (x,), g[i])) + ' (%2d) %2d' % (self.correct[i], self.left[i]) + '\n'
        return s

    def formatted_repr(self):
        return '\n'.join(''.join(map(str, self.guess[i])) + ';%d' % (self.correct[i],) for i in xrange(self.m))
    
    @property
    def m(self): return self.guess.shape[0]
    @property
    def n(self): return self.guess.shape[1]
    @property
    def is_filled(self): return self.guess.size == 0 or self.num_seq_filled == self.n
    @property
    def num_seq_filled(self): return len(np.where(self.seq != X)[0])
    
    @property
    def is_infeasible(self):
        '''Is the position infeasible or not?'''
        # Check that in each guess the number of corrects is not greater than the number of
        # left digits (those that are not determined to be wrong)
        return any(self.left < self.correct)

    @property
    def best_row(self):
        '''Row of top priority in DFS.'''
        top_priority_row, min_priority = None, None
        for k, v in enumerate(zip(self.correct, self.left)):
            if not min_priority or v < min_priority: top_priority_row, min_priority = k, v
        return top_priority_row
            
    def copy(self):
        '''Return a deep copy of this object.'''
        return Position(self.guess.copy(), self.correct.copy(), self.seq.copy(), self.depth + 1, wrong=[set(x) for x in self.wrong])
    
    def remove_zero_rows(self):
        '''Remove zero rows and cross-out all entries equal to them in each column.'''
        g = self.guess
        zero_rows = (self.correct == 0)
        if any(zero_rows):
            for i in np.where(zero_rows)[0]: 
                for j, value in enumerate(g[i]):
                    if value != X: self.wrong[j].add(value)
                g[g == g[i]] = X
            nz_rows = ~zero_rows
            self.guess, self.correct, self.left = self.guess[nz_rows], self.correct[nz_rows], self.left[nz_rows] 
            self.left = np.sum(self.guess != X, 1)
            
    def set_digit(self, j, value):
        '''Set the correct value of digit j to ''value''.'''
        gj = self.guess[:, j]
        eq = (gj == value)
        # Cross-out incorrect as well as correct values. Memorize correct value in the seq field.
        self.guess[:, j] = X
        self.correct[eq] -= 1
        self.seq[j] = value
        self.left = np.sum(self.guess != X, 1)
        self.remove_zero_rows()

def _search(position):
    '''Depth-First Search (DFS) for a solution. Once found, the search is terminated, since we
    are guaranteed solution uniqueness by the problem statement.'''
    if position.is_infeasible:
        return None
    if position.is_filled:
        seq = position.seq
        # Set free digits to an arbitrary non-conflicting value
        for j in np.where(seq == X)[0]:
            seq[j] = np.setdiff1d(np.arange(10), position.wrong[j])[0]
        return seq

    # Recursion: branch to all possible combinations of correct digits in the row that has the
    # least number of branches (a DFS ordering heuristic that hopefully leads to an efficient search)
    i = position.best_row
    gi = position.guess[i]
    if len(np.where(gi != X)[0]) == 0: raise ValueError('No corrects in best row!')
    for values in combinations(np.where(gi != X)[0], position.correct[i]):
        p = position.copy()
        for j in values: p.set_digit(j, gi[j])
        solution = _search(p)
        if solution is not None: return solution
    return None  # No solution was found in the entire DFS search

'''Methods to check a solution.'''
residual = lambda (g, c), x: c - np.sum(np.tile(x, (g.shape[0], 1)) == g, axis=1)
ssq = lambda r: np.sum(r * r)

def solve (g, correct):
    '''Main DFS driver call.'''
    solution = _search(Position(g, correct, np.tile(np.byte(X), (g.shape[1],))))
    r = ssq(residual((g, correct), solution)) if solution is not None else -1
    return ''.join(map(str, solution)) if solution is not None and r == 0 else None

def read_position(file_name):
    '''Read guesses from a text file.'''
    data = np.loadtxt(open(file_name, 'rb'), delimiter=';', dtype=str)
    m = data.shape[0]
    correct = data[:, 1].astype(np.byte)
    g = np.empty((m, len(data[0, 0])), dtype=np.byte)
    for i in xrange(m): g[i] = map(np.byte, data[i, 0])
    return g, correct

def generate_test_set(m, n, max_c):
    '''Generate a test set. Not guaranteed to have a unique solution.''' 
    digits = np.arange(10)
    x = np.random.randint(0, 10, (n,))
    g = np.zeros((m, n), dtype=int)
    c = np.random.randint(0, max_c + 1, (m,))
    location = np.arange(n)
    for i in xrange(m):
        correct_digits = np.random.choice(location, c[i], replace=False)
        g[i, correct_digits] = x[correct_digits]
        for j in np.setdiff1d(location, correct_digits): g[i, j] = np.random.choice(np.setdiff1d(digits, x[j]))
    return (g, c), x

def test_random_test_sets():
    '''Run randomized testing.'''
    for _ in xrange(50):
        (g, c), x0 = generate_test_set(5, 3, 2)
        p = Position(g, c, np.tile(np.byte(X), (g.shape[1],)), remove_zero_rows=False)
        x = solve(g.copy(), c.copy())
        if x is None:
            print p.formatted_repr()
            print 'x0', repr(x0)
            print 'x', repr(x)
            print 'Testing: FAIL'
            return
    print 'Testing OK'
    
if __name__ == "__main__":
    test_random_test_sets()
    
    for file_name in ['problem185-small.dat',
                 'problem185-small2.dat',
                 'problem185-moderate.dat',
                 'problem185-moderate2.dat',
                 'problem185-large.dat',
                 ]:
        print solve(*read_position(file_name))

# ----------------- Relaxation solution - trapped in local minimum --------------------
# 
# def relax(p, x):
#     g, _ = p
#     for j in xrange(g.shape[1]):
#         #r_old = ssq(residual(p, x))
#         k = 0
#         x[j] = k        
#         r_min, j_min = ssq(residual(p, x)), k
#         for k in xrange(1, 10):
#             x[j] = k
#             r = ssq(residual(p, x))
#             if r < r_min: r_min, j_min = r, k
#         x[j] = j_min
#         #print '\t', j, j_min, x, r_min, r_old
#     return x
# 
# def solve2(p, max_iter=100):
#     print p[0].shape[1]
#     x = np.random.randint(0, 10, (p[0].shape[1],))
#     x = np.array([3, 9, 4, 4, 2])
#     for _ in xrange(max_iter):
#         x = relax(p, x)
#         r = ssq(residual(p, x))
#         print x, r
#         if r == 0: return x
#     return None
