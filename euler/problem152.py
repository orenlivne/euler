'''
============================================================
http://projecteuler.net/problem=152

There are several ways to write the number 1/2 as a sum of inverse squares using distinct integers.
For instance, the numbers {2,3,4,5,7,12,15,20,28,35} can be used:
In fact, only using integers between 2 and 45 inclusive, there are exactly three ways to do it, the remaining two being: {2,3,4,6,7,9,10,20,28,35,36,45} and {2,3,4,6,7,9,12,15,28,30,35,36,45}.
How many ways are there to write the number 1/2 as a sum of inverse squares using distinct integers between 2 and 80 inclusive?
============================================================
'''
import itertools as it, numpy as np
from fractions import Fraction
from problem007 import primes

def combos(k):
    '''Return all combinations of numbers in 1..k and their sum of inverse squares.'''
    l_list = np.arange(1, k + 1)
    for S in it.product((False, True), repeat=k):
        f = sum(Fraction(1, n * n) for n in l_list[np.where(S)])
        yield np.array(S), f

def valid_combos(N, K, debug=False):
    '''Return all valid combinations of multiples of large primes (> N/K) in an inverse squares sum
    summing up to 0.5; a boolean array of appearance status (1=present, never present=0, -1=unknown),
    list of remaining primes <= N/K, and the list of unknown numbers in 2..N. K should be chosen
    to balance the runtimes of this method and the subsequent DFS'''
    
    p_list, left, bound, x, c, T = \
    primes('lt', N + 1), 0, float(N) / K, -np.ones((N + 1), dtype=int), [], \
    [None] + [list(combos(k)) for k in xrange(1, K + 1)]
    num_primes = len(p_list)
    known = set([])
    while left < num_primes and p_list[left] < bound: left += 1
    if debug: print 'N', N, 'K', K, 'All primes', p_list
    for p in p_list[left:]:
        k, p2 = N / p, p * p
        valid = [(np.array([(l + 1) * p for l in np.where(S)[0]]),
                  np.array([(l + 1) * p for l in np.where(~S)[0]]),
                  f / p2) for S, f in T[k] if f.numerator % p2 == 0]
        if valid:
            c.append(valid)
            if debug: print 'p', p, 'k', k, 'admissible combos', len(valid)
            for y in valid: print '\t', y
            known |= set([l * p for l in xrange(1, k + 1)])
        else: x[p::p] = 0
    c = [[(S, T, float(f)) for S, T, f in y] for y in c]
    unknown = np.array(sorted((set(np.where(x < 0)[0]) - known) - set([0, 1])))
    known = sorted(known)
    if debug: 
        print 'len(c)', len(c)
        print 'known (%d)' % (len(known,)), known
        print 'unknown (%d)' % (len(unknown,)), unknown
    return x, c, p_list[:left], unknown

is_compatible = lambda S, T, x: all(x[n] != 0 for n in S) and all(x[n] != 1 for n in T)

def dfs_combos(r, path, x, c, small_primes, depth=0, debug=False):
    '''Depth-first search in combinations of large primes.'''
    if debug: print '   ' * depth, 'r', r, 'path', sorted(path), 'depth', depth, 'x', list(x)
    if abs(r) < 1e-12: yield path
    elif r > 0:
        path_old = path.copy()
        if depth < len(c):
            if debug: 
                print '   ' * depth, 'compatible', [(S, T, f) for S, T, f in c[depth] if is_compatible(S, T, x)]
                print '   ' * depth, 'incompatible', [(S, T, f) for S, T, f in c[depth] if not is_compatible(S, T, x)]
            for S, T, f in ((S, T, f) for S, T, f in c[depth] if is_compatible(S, T, x)):
                path_new = path_old | set(list(S))
                rf = 0.5 - sum(1. / (n * n) for n in path_new)
                y = x.copy()
                if S.size: y[S] = 1
                if T.size: y[T] = 0
                for path in dfs_combos(rf, path_new, y, c, small_primes, depth=depth + 1, debug=debug): yield path
        else:
            # Singles children branches
            f = sum(Fraction(1, n * n) for n in path)
            b = f.denominator
            for p in small_primes:
                while b % p == 0: b /= p
            denom_ok = (f.numerator == 0) or (b == 1)
            if denom_ok: yield path, f

def dfs_singles(r, path, a, b, depth=0, debug=False):
    '''A leaf of the depth-first search in combinations of large primes: depth-first search
    within ''singles'' = element of the ''unknown'' array.'''
    if abs(r) < 1e-12: yield path
    elif r > 0:
        i_min, i_max = 0, len(a)
        try: i_min = it.dropwhile(lambda (_, x): 1 - 1e-10 > r * x * x, enumerate(a)).next()[0]
        except StopIteration: i_min = len(a)
        try: i_max = it.dropwhile(lambda (_, x): x > r - 1e-10, enumerate(b)).next()[0]
        except StopIteration: i_max = len(a)
        for i in xrange(i_min, i_max):
            for p in dfs_singles(r - 1. / (a[i] * a[i]), path | set([a[i]]), a[i + 1:], b[i + 1:], debug=debug): yield p
            
def num_ways(N, K, debug=False):
    '''Main call. Number of ways to make 0.5 with the numbers 2..N. See comment above about the choice
    of K. K should slowly increase with N. In the future, we could add code to optimize its choice.'''
    x, c, small_primes, a = valid_combos(N, K, debug=debug)
    a, b = list(a), list(np.flipud(np.cumsum(np.flipud(1. / (a * a)))))
    ok_combos = list(dfs_combos(0.5, set([]), x, c, small_primes, debug=debug))
    for k, (S, f) in enumerate(ok_combos):
        if debug: print 'combo %d/%d' % (k, len(ok_combos)), sorted(S), f
        for path in dfs_singles(0.5 - float(f), S, a, b, debug=debug):
            if np.abs(sum(1. / (n * n) for n in path) - 0.5) > 1e-12:
                raise ValueError('Spurious solution ' + repr(sorted(path)))
            print sorted(path)
            yield sorted(path)

if __name__ == "__main__":
    print len(list(num_ways(80, 16, debug=False)))
