'''
============================================================
http://rosalind.info/problems/sort

A reversal of a permutation can be encoded by the two indices at the endpoints of the interval that it inverts; for example, the reversal that transforms (4,1,2,6,3,5) into (4,1,3,6,2,5) is encoded by [3,5].

A collection of reversals sorts p into g if the collection contains drev(p,g) reversals, which when successively applied to p yield g.

Given: Two permutations p and g, each of length 10.

Return: The reversal distance drev(p,g), followed by a collection of reversals sorting p into g. If multiple collections of such reversals exist, you may return any one.

============================================================
'''
from collections import deque
import os, rosalind.rosalind_rear as rr

def all_reverses_with_moves(p):
    '''A generator of all possible reverses of a permutation p.'''
    n = len(p)
    return ((rr.reverse(p, (j, k)), (j, k)) for j in xrange(n - 1) for k in xrange(j + 2, n + 1))

def reversal_distance_hash(n):
    '''Return the shortest path length (=reversal distance) between the identity permutation
    and every permutation of length n. Note that d(t,s) = d(s,t).'''
    # Permutations are encoded as tuples.
    i = tuple(xrange(n))  # Identity permutation
    # Breadth-first search (BFS) 
    q, count, d = deque([i]), 0, {i: (0, -1, -1)}  # d = Reversal distance dictionary. d[p] = d(p,i)
    while q:
        count += 1
        if count % 100000 == 0: print count, 'queue size', len(q) 
        x = q.popleft()
        dy = d[x][0] + 1
        for y, move in all_reverses_with_moves(x):
            if not y in d:
                d[y] = (dy, move[0], move[1])
                # print y, d[y], 'came from', x
                q.append(y)
    return d
    
def read_path_hash(file_name):
    with open(file_name, 'rb') as f:
        return dict((tuple(map(int, x[:-3])), (int(x[-3]), int(x[-2]), int(x[-1]))) for x in (x.split() for x in f))

def write_path_hash(n, d, file_name):
    with open(file_name, 'wb') as f:
        for k, v in sorted(d.iteritems()):
            f.write('%s %d %d %d\n' % (' '.join(map(str, k)), v[0], v[1], v[2]))

def read_or_create_reversal_path_hash(n):
    file_name = 'reversal_path_%d.txt' % (n,)
    if os.path.exists(file_name): d = read_path_hash(file_name)
    else:
        d = reversal_distance_hash(n)
        write_path_hash(n, d, file_name)
    return d

def _reversal_sort_log(d, p):
    '''Print a shortest path log from the identity permutation to the permutation p.'''
    d_rev, start, stop = d[p]
    print d_rev  
    print start + 1, stop
    for _ in xrange(d_rev - 1):
        p = rr.reverse(p, (start, stop))
        _, start, stop = d[p]
        print start + 1, stop
        
def reversal_sort_log(d, s, t):
    '''Print a shortest path log from the permutation s to the permutation t.'''
    _reversal_sort_log(d, rr.pmult(rr.pinv(t), s))
    
def ros_sort(file_name):
    '''Solution to the question. Prepares a hash d if doesn\'t exist yet, then fetches the entries
    of t^{-1}*s from d to find reversal_distance(t,s).'''
    with open(file_name, 'rb') as f: s, t = rr.to_int_list(f.next()), rr.to_int_list(f.next())
    d = read_or_create_reversal_path_hash(len(s))
    reversal_sort_log(d, s, t)

if __name__ == "__main__":
#     d = read_or_create_reversal_path_hash(5)
#     reversal_sort_log(d, (4, 1, 3, 0, 2), (1, 2, 0, 4, 3))
#     ros_sort('rosalind_sort_sample1.dat')
    ros_sort('rosalind_sort_sample.dat')
    ros_sort('rosalind_sort.dat')
