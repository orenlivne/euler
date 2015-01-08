'''
============================================================
http://projecteuler.net/problem=178

Consider the number 45656. 
It can be seen that each pair of consecutive digits of 45656 has a difference of one.
A number for which every pair of consecutive digits has a difference of one is called a step number.
A pandigital number contains every decimal digit from 0 to d-1 at least once.
How many pandigital step numbers less than 10**40 are there?
============================================================
'''
#------------------- Graph-based solution, broken -------------------
# import numpy as np, networkx as nx
# 
# def transition_graph(d):
#     g = nx.DiGraph()
#     g.add_nodes_from(node_list(d))
#     g.add_edges_from(edge_list(d))
#     return g
# 
# def node_list(d):
#     for i in xrange(d):
#         for j in (j for j in xrange(d) if i <= j):
#             for k in xrange(d):
#                 yield (i, j, k)
#     
# def edge_list(d):
#     for i in xrange(d):
#         for j in (j for j in xrange(d) if i <= j):
#             for k in xrange(1, d):
#                 yield (i, j, k), (min(i, k - 1), max(j, k - 1), k - 1)
#             for k in xrange(0, d - 1):
#                 yield (i, j, k), (min(i, k + 1), max(j, k + 1), k + 1)

#------------------- Brute force, for validation -------------------
# import itertools as it
# 
# is_sum_step_pan_str = lambda x, d: all(digit in x for digit in xrange(d)) and \
# all(x[i + 1] == x[i] - 1 or x[i + 1] == x[i] + 1 for i in xrange(len(x) - 1))
# 
# sum_step_pan_list = lambda d, n: [''.join(it.imap(str, x)) for x in it.product(xrange(1, d),
#                                                          *(xrange(d) for _ in xrange(n - 1)))
#                                    if is_sum_step_pan_str(x, d)] 
# 
# sum_step_pan_bf = lambda d, n: sum(1 for l in xrange(1, n + 1) for x in 
#                                    it.product(xrange(1, d), *(xrange(d) for _ in xrange(l - 1)))
#                                    if is_sum_step_pan_str(x, d)) 
# 
# def test_vs_brute_force():
#     d = 4
#     for n in xrange(1, 11):
#         print 'n', 'fast', sum_step_pan(d, n), 'bf', sum_step_pan_bf(d, n)
#         print '  ', sum_step_pan_list(d, n)

#------------------- Fast solution -------------------
import numpy as np

def initial_condition(d):
    '''Dynamic programming initialization (length-1 numbers).'''
    x = np.zeros((d, d, d), dtype=long)
    for k in xrange(1, d): x[k, k, k] = 1
    return x

def transition(x, d):
    '''Dynamic programming transition from length-(n-1) to length-n numbers. State (i,j,k)
    is the number of step numbers whose min digit is i, max digit is j and end with k.
    Note that i<=j and that the number must contain all digits between i and j, inclusive,
    because it is a step number.'''
    y = np.zeros_like(x, dtype=long)
    for i in xrange(d):
        for j in xrange(i, d):
            for k in xrange(1, d): y[min(i, k - 1), max(j, k - 1), k - 1] += x[i, j, k]
            for k in xrange(0, d - 1): y[min(i, k + 1), max(j, k + 1), k + 1] += x[i, j, k]
    return y

'''Relevant states that contribute to the desired quantity (min digit=0, max digit=9 <==>
pandigital).'''
state_sum = lambda x, d: sum(x[0, d - 1, :])
 
def sum_step_pan(d, n):
    '''Loop over number lengths 1,2,...,n and calculate the number of step numbers that are also
    pandigital. d = number of digits in the alphabet (d=2: binary; d=10: decimal).''' 
    x = initial_condition(d)
    s = state_sum(x, d)  # For symmetry, although this is hardly needed, as s=0 for all d and n=1 
    for _ in xrange(2, n + 1): 
        x = transition(x, d)
        s += state_sum(x, d)
    return s

if __name__ == "__main__":
    print sum_step_pan(10, 40)
