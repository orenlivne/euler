'''
============================================================
http://rosalind.info/problems/rear

Given: A collection of at most 5 pairs of permutations, all
of which have length 10.

Return: The reversal distance between each permutation pair.
============================================================
'''
from collections import deque
import os, sys

def reverse(p, (j, k)):
    '''Reverse the interval p[j:k] in the permutation p.'''
    p_copy = list(p)
    p_copy[j:k] = p[k - 1:j - 1:-1] if j else p[k - 1::-1]
    return tuple(p_copy)

def all_reverses(p):
    '''A generator of all possible reverses of a permutation p.'''
    n = len(p)
    return (reverse(p, (j, k)) for j in xrange(n - 1) for k in xrange(j + 2, n + 1))

def reversal_distance_hash(n):
    '''Return the shortest path length (=reversal distance) between the identity permutation
    and every permutation of length n. Note that d(t,s) = d(s,t).'''
    # Permutations are encoded as tuples.
    i = tuple(xrange(n))  # Identity permutation
    # Breadth-first search (BFS) 
    q, count, d = deque([i]), 0, {i: 0}  # d = Reversal distance dictionary. d[p] = d(p,i)
    while q:
        count += 1
        if count % 100000 == 0: print count, 'queue size', len(q) 
        x = q.popleft()
        dy = d[x] + 1
        for y in all_reverses(x):
            if not y in d:
                d[y] = dy
                q.append(y)
    return d
    
def read_hash(file_name):
    with open(file_name, 'rb') as f:
        return dict((tuple(map(int, x[:-1])), int(x[-1])) for x in (x.split() for x in f))
    
def write_hash(n, d, file_name):
    with open(file_name, 'wb') as f:
        for k, v in sorted(d.iteritems()):
            f.write('%s %d\n' % (' '.join(map(str, k)), v))

def read_or_create_reversal_distance_hash(n):
    file_name = 'reversal_distance_%d.txt' % (n,)
    if os.path.exists(file_name): d = read_hash(file_name)
    else:
        d = reversal_distance_hash(n)
        write_hash(n, d, file_name)
    return d

'''Convert space-delimited 1-based permutation string to 0-based permutation.'''
to_int_list = lambda s: map(lambda x: int(x) - 1, s.split())

def pinv(a):
    '''Inverse permutation of a.'''
    n = len(a)
    b = [0] * n
    for i in xrange(n): b[a[i]] = i
    return tuple(b)

def pmult(a, b):
    '''Multiply (compose) permutations: a o b.'''
    n = len(a)
    c = [0] * n
    for i in xrange(n): c[i] = a[b[i]]
    return tuple(c)

def rev_dist(s, t, d):
    '''Return the reversal distance of permutations s, t. Fetch from the hash d.'''
    return d[pmult(pinv(t), s)]

def rear(file_name, debug=0):
    '''Solution to the question. Prepares a hash d if doesn\'t exist yet, then fetches the entries
    of t^{-1}*s from d to find reversal_distance(t,s).'''
    d = None
    with open(file_name, 'rb') as f:
        while True:
            try:
                s, t = to_int_list(f.next()), to_int_list(f.next())
                if not d: d = read_or_create_reversal_distance_hash(len(s))
                sys.stdout.write('%d' % (rev_dist(s, t, d),))
                f.next()  # Blank line in file - separates entries
                sys.stdout.write(' ')  # If exists, separate output distances
            except StopIteration: break
            
if __name__ == "__main__":
    d = read_or_create_reversal_distance_hash(5)
    print rev_dist((4, 1, 3, 0, 2), (1, 2, 0, 4, 3), d)
    #rear('rosalind_rear_sample.dat', debug=1)
    #rear('rosalind_rear.dat', debug=1)
