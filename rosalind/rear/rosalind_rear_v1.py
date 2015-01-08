'''
============================================================
http://rosalind.info/problems/rear

Given: A collection of at most 5 pairs of permutations, all
of which have length 10.

Return: The reversal distance between each permutation pair.
============================================================
'''
import sys

def is_breakpoint(p, j, k=None, replaces_left=None):
    '''Returns 0 if breakpoint, else 1.'''
    n = len(p)
    if j == 0:  # Case A
        p_left = p[k] if k is not None else p[j] 
        return 0 if p_left == 0 else 1
    elif j == n:  # Case B
        p_right = p[k] if k is not None else p[n - 1]
        return 0 if p_right == n - 1 else 1
    else:
        if k is not None:
            if replaces_left: dp = p[j] - p[k]  # Case C1
            else: dp = p[k] - p[j - 1]  # Case C2
        else: dp = p[j] - p[j - 1]
        return 0 if dp == 1 or dp == -1 else 1

'''Convert space-delimited 1-based permutation string to 0-based permutation.'''
to_int_list = lambda s: map(lambda x: int(x) - 1, s.split())

def pinv(a):
    '''Inverse permutation of a.'''
    n = len(a)
    b = [0] * n
    for i in xrange(n): b[a[i]] = i
    return b

def pmult(a, b):
    '''Multiply (compose) permutations: a o b.'''
    n = len(a)
    c = [0] * n
    for i in xrange(n): c[i] = a[b[i]]
    return c

def rev_dist(s, t, debug=0):
    '''Return the reversal distance of permutations s, t using a Greedy approach.
    O(n^3) worst case runtime.'''
    p, n = pmult(pinv(t), s), len(s)
    b, d = sum(is_breakpoint(p, i) for i in xrange(n + 1)), 0
    if debug:
        print 's', s
        print 't', t
        print 't^-1', pinv(t)
        print p, 'd', d, 'b', b
    return _rev_dist(p, b, debug=debug)

def _rev_dist(p, b, d=0, debug=0, depth=0):
    '''Return the reversal distance of permutations s, t using a Greedy approach.
    O(n^3) worst case runtime.'''
    if debug: print p, 'b', b, 'd', d, 'depth', depth
    if b == 0: return d
    n = len(p)
    if debug >= 2:
        for j in xrange(n - 1):
            for k in xrange(j + 2, n + 1):
                a0 = is_breakpoint(p, j, k - 1, False)
                a1 = is_breakpoint(p, j)
                a2 = is_breakpoint(p, k, j, True)
                a3 = is_breakpoint(p, k)
                print '\t', (j, k), a0, '-', a1, '+', a2, '-', a3, '-> db', a0 - a1 + a2 - a3
    options = [(is_breakpoint(p, j, k - 1, False) - is_breakpoint(p, j) + 
                is_breakpoint(p, k, j, True) - is_breakpoint(p, k), (j, k))
                for j in xrange(n - 1) for k in xrange(j + 2, n + 1)]
    min_db = min(options)[0]
    min_moves = [(j, k) for db, (j, k) in options if db == min_db]
    if debug:
        print '\t', 'min_db', min_db, 'min_moves', min_moves 
    
    d_min = None
    d += 1
    b += min_db
    for j, k in min_moves:
        p_copy = list(p)
        p_copy[j:k] = p[k - 1:j - 1:-1] if j else p[k - 1::-1]
        print '\t', 'Making the move', (j, k) 
        d_move = _rev_dist(p_copy, b, d, debug=debug, depth=depth + 1)
        if d_min is None or d_move < d_min: d_min = d_move
        # if d > n + 1: raise ValueError('We shouldn\'t be here')
    return d_min

def rear(file_name, debug=0):
    with open(file_name, 'rb') as f:
        while True:
            try:
                s, t = to_int_list(f.next()), to_int_list(f.next())
                sys.stdout.write('%d' % (rev_dist(s, t, debug=debug),))
                f.next()  # Blank line in file - separates entries
                sys.stdout.write(' ')  # If exists, separate output distances
            except StopIteration: break
            
if __name__ == "__main__":
    rear('rosalind_rear_sample5.dat', debug=1)
