'''
============================================================
http://rosalind.info/problems/fibd/

Problem

Figure 4. A figure illustrating the propagation of Fibonacci's rabbits if they die after three months.
Recall the definition of the Fibonacci numbers from "Rabbits and Recurrence Relations", which followed the recurrence relation Fn=Fn-1+Fn-2 and assumed that each pair of rabbits reaches maturity in one month and produces a single pair of offspring (one male, one female) each subsequent month.

Our aim is to somehow modify this recurrence relation to achieve a dynamic programming solution in the case that all rabbits die out after a fixed number of months. See Figure 4 for a depiction of a rabbit tree in which rabbits live for three months (meaning that they reproduce only twice before dying).

Given: Positive integers n<=100 and m<=20.

Return: The total number of pairs of rabbits that will remain after the n-th month if all rabbits live for m months.
============================================================
'''
from rosalind.rosutil import read_ints_str
import itertools as it
from collections import deque

def fibd_wrong(m, f1=1L, f2=1L):
    '''Generalized Fibonacci sequence generator. Wrong, you cannot die twice.'''
    m1 = m + 1; f = [0] * (m + 1); f[0] = f1; f[1] = f2; yield f1; yield f2; n = 1
    while True:
        n = (n + 1) % m1
        f[n] = f[(n - 1) % m1] + f[(n - 2) % m1] - f[(n + 1) % m]
        yield f[n]
    
def fibd(m):
    '''Generalized Fibonacci sequence generator.'''
    g, f = deque([1L] + [0L] * (m - 1)), 1  # g = state vector, g[i] = #rabbits of age i+1. f = total #rabbits
    while True:
        yield f
        # Advance state to next time step
        old = g.pop()  # The old die
        young = f - g[0]  # Everyone except recently born make a copy (including the old that make a copy right before dying at this timestep) = # rabbits in newest generation
        g.appendleft(young)  # Add new generation; older generations grow older by 1 (i.e., right-shifted)
        f += (young - old)  # Update total
    
def nth_fibd(file_name):
    '''Main call.'''
    n, m = read_ints_str(file_name) 
    print '%d' % (it.islice(fibd(m), n - 1, n).next(),)
    
if __name__ == "__main__":
    nth_fibd('rosalind_fibd_sample.dat')
    nth_fibd('rosalind_fibd.dat')
