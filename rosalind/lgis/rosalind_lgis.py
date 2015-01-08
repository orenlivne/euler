#!/usr/bin/env python
'''
============================================================
http://rosalind.info/problems/lgis

A subsequence of a permutation is a collection of elements of the permutation in the order that they appear. For example, (5, 3, 4) is a subsequence of (5, 1, 3, 4, 2).

A subsequence is increasing if the elements of the subsequence increase, and decreasing if the elements decrease. For example, given the permutation (8, 2, 1, 6, 5, 7, 4, 3, 9), an increasing subsequence is (2, 6, 7, 9), and a decreasing subsequence is (8, 6, 5, 4, 3). You may verify that these two subsequences are as long as possible.

Given: A positive integer n <= 10000 followed by a permutation Pi of length n.

Return: A longest increasing subsequence of Pi, followed by a longest decreasing subsequence of Pi.

Sample Dataset

5
5 1 4 2 3
Sample Output
1 2 3
5 4 2
============================================================
'''
#---------------------------------------
# Dynamic Programming Solution - wrong
#---------------------------------------
def longest_subsequence_dp(a, sign):
    '''Return the longest increasing (if sign=1) or decreasing (if sign=-1) sub-sequence in the
    permutation a of the first n natural integers. Time and storage are O(n). If multiple longest
    sub-sequences exist, arbitrarily returns one of them.'''
    # Solution by dynamic programming: the longest sequences either include the maximal element x
    # or doesn't. If they don't, they must be the longest sequences in the list b where x is removed.
    # If they do, they are one element shorter in b. So if the longest sequence in b has length m,
    # we keep track of all sequences of lengths m-1 and m. Passing from b to a, we append the max
    # element to all lists whose last element's ind value is less than n's (for the increasing case;
    # greater than, for the decreasing case), update m, and throw away lists of size < m-1.
    #
    # In practice, it is faster to start with the minimum element and build up instead of a recursive
    # algorithm (bottom-up dynamic programming).
    #
    # Note that we never need to explicitly sort a, since it is a permutation. We know that the
    # max element is n, the next one is n-1, etc.
    
    # Create the inverse permutation ind of a (but 0-based, since python lists are). That is,
    # ind[x] is the index of the number x in the list a.' 
    S, n = set([]), len(a)
    ind = [None] * n
    if sign > 0:
        for i in xrange(n): ind[a[i] - 1] = i
    else:
        for i in xrange(n): ind[a[i] - 1] = n - 1 - i
    # Loop over elements, smallest-to-largest (for the increasing case; vice versa for the
    # decreasing case) and update the list of longest sequences (or potentially extensible sequences) S
    for x in (xrange(1, n + 1) if sign > 0 else xrange(n, 0, -1)):
        ind_x, sx = ind[x - 1], (x,)
        S.add(sx)
        T = S.copy()
        for s in T:
            S.add(s + sx if sign * (ind_x - ind[s[-1] - 1]) > 0 else s)
        # print 'x', x, 'ind_x', ind_x, '|S|', len(S), 'S', S
        S = set(S)
    m = max(map(len, S))
    S = filter(lambda s: len(s) == m, S)
    # print S
    return S[0]

read_seq = lambda f: map(int, open(f, 'rb').readlines()[1].rstrip('\n').rstrip('\r').split(' '))

def sequences(solver, a):
    '''Return a tuple of the longest increasing and longest decreasing sub-sequences in the
    permutation a of the first n natural integers.'''
    inc = solver(a, 1)
    print inc
    print len(inc) 
    dec = solver(a, -1)
    print dec
    print len(dec)
    return tuple((' '.join(map(str, inc)), ' '.join(map(str, dec))))

#---------------------------------------
# Directed A-cyclic Graph (DAG) solution
#---------------------------------------
import networkx as nx, numpy as np, itertools as it

def build_dag(a):
    '''Build a DAG, where an edge from x to y means that x and y can be consecutive elements in the longest
    increasing sub-sequence.'''
    # print 'a', a
    n = len(a)
    c_all = np.zeros((n,), dtype=np.bool)  # A flag array. c[i] indicates that y can be after after x
    G = nx.DiGraph() 
    for i, x in enumerate(a):
        # print 'i', i, 'x', x
        # For each number in the sequence, examine all its successors y and determine if
        # we can "jump" from x to y. This can happen if y > x and if there is no intermediary
        # z between x and y in a such that x < z < y.
        c = c_all[i + 1:]  # Restrict view to x's sucessors 
        c[:] = True  # Initially, every y is a candidate to be next to
        c[np.where(a[i + 1:] < x)[0]] = False  # Remove all those that can't be after x because they are smaller        
        # print '\tc', c.astype(int)

        p = i + 1  # A pointer into a, points to the next location to be examined among x's successors
        while p < n and not c_all[p]:
            p += 1
        
        while p < n: 
            y = a[p]
            # print '\tp', p, 'y', y, 'c', c.astype(int)
            # print '\t\ta[p+1:]', a[p + 1:], 'where', np.where(a[p + 1:] > y)[0] + p + 1
            c_all[np.where(a[p + 1:] > y)[0] + p + 1] = False  # Remove all those for which y would be an intermediary
            # print '\t       After pass, c', c.astype(int)
            p += 1  # Advance pointer to the next candidate (i.e. whose flag value is still True)
            while p < n and not c_all[p]:
                p += 1
        successors = a[np.where(c)[0] + i + 1]
        # print '\tx=%d can jump to %s' % (x, repr(successors))
        G.add_edges_from(it.product([x], successors))
    return G

def longest_path_length(G):
    '''Return an array (of size n+1; dummy 0th entry set to 0) where a[i] = length of longest path in the DAG G whose
    nodes are the values 1..n.'''
    depth = np.zeros((G.number_of_nodes() + 1,), dtype=np.uint)
    for x in nx.topological_sort(G):
        # print 'x', x, 'in-degree', G.in_degree(x)
        if G.in_degree(x) > 0:
            depth[x] = max(depth[y] for y in G.predecessors(x)) + 1
    return depth
    
def longest_subsequence_dag(a, sign):
    '''Return a longest increasing (if sign=1) or decreasing (if sign=-1) sub-sequence in the
    permutation a of the first n natural integers. Time and storage are O(n). If multiple longest
    sub-sequences exist, arbitrarily returns one of them.'''

    # Dan Cook's idea: use symmetry to solve the decreasing case in terms of the increasing case 
    if sign < 0:
        return list(reversed(longest_subsequence_dag(list(reversed(a)), 1)))
    
    G = build_dag(np.array(a))  # Construct a DAG whose edges represent all candidate pairs of consecutive elements of the longest subsequence
    assert nx.is_directed_acyclic_graph(G)
    # print 'Edges', G.edges()

    depth = longest_path_length(G)  # For each node, calculate the longest path length       
    # print 'depth', depth 
    
    # Back-track from a node of maximum depth to its ancestors to reconstruct the longest path
    x = np.argmax(depth)
    seq = [x]
    # print 'x', x, 'depth', depth[x]
    while G.in_degree(x) > 0:
        # To find the maximum path, choose a parent of minimum depth
        parents = G.predecessors(x)
        # print 'parents', parents
        x = parents[np.argmax(depth[parents])]
        # print 'x', x, 'depth', depth[x]
        seq.append(x)
        # print 'seq', seq
    # print 'final seq', list(reversed(seq))
    return list(reversed(seq))

#---------------------------------------
# Testing
#---------------------------------------
from numpy import random

def randperm(n):
    '''Generate a random permutation of 1..n.'''
    x = range(1, n + 1)
    random.shuffle(x)
    return x
   
all_subsets = lambda S: it.chain(*(it.combinations(S, m) for m in xrange(1, len(S) + 1)))
increasing = lambda a: all(a[i] < a[i + 1] for i in xrange(len(a) - 1))
decreasing = lambda a: all(a[i] > a[i + 1] for i in xrange(len(a) - 1))

def longest_elements(S):
    '''S = list of lists, sorted by increasing length.'''
    m = len(S[-1])
    for a in reversed(S):
        if len(a) == m:
            yield a
        else:
            break

def check_sequences(solver, a):
    '''Compare our solution with brute-force.''' 
    assert tuple(solver(a, 1)) in list(longest_elements(filter(increasing, all_subsets(a))))
    assert tuple(solver(a, -1)) in list(longest_elements(filter(decreasing, all_subsets(a))))

if __name__ == "__main__":
    tests = [
             [9, 3, 7, 2, 4, 5, 8, 1, 10, 6],
             [5, 1, 4, 2, 3],
             [7, 5, 4, 6, 1, 2, 3],
             [3, 4, 5, 1, 2],
             [3, 2, 1, 5, 4],
             [5, 1, 4, 2, 3, 7, 6],
             [10, 8, 9, 5, 1, 4, 2, 3, 7, 6]
             ]

#    solver = longest_subsequence_dp
    solver = longest_subsequence_dag
    for a in tests:
        check_sequences(solver, a)
    check_sequences(solver, randperm(10))
    
    print '\n'.join(sequences(solver, read_seq('rosalind_lgis_sample.dat')))
    import time
    start_time = time.time()
    print '\n'.join(sequences(solver, read_seq('rosalind_lgis3.dat')))
    print time.time() - start_time, 'sec'
