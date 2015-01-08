'''
============================================================
http://projecteuler.net/problem=100

If a box contains twenty-one coloured discs, composed of fifteen blue discs and six red discs, and two discs were taken at random, it can be seen that the probability of taking two blue discs, P(BB) = (15/21)(14/20) = 1/2.

The next such arrangement, for which there is exactly 50% chance of taking two blue discs at random, is a box containing eighty-five blue discs and thirty-five red discs.

By finding the first arrangement to contain over 1012 = 1,000,000,000,000 discs in total, determine the number of blue discs that the box would contain.
============================================================
'''
from problem094 import pell_solutions
from itertools import dropwhile

def min_balls(N):
    a_min = (1 + 2 * N * (N - 1)) ** 0.5
    return (1 + dropwhile(lambda (_, a): a <= a_min, pell_solutions(2, -1)).next()[1]) / 2

if __name__ == "__main__":
    print min_balls(10 ** 12) # 756872327473
    
