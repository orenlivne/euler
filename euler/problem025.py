'''
============================================================
http://projecteuler.net/problem=25

The Fibonacci sequence is defined by the recurrence relation:

Fn = Fn1 + Fn2, where F1 = 1 and F2 = 1.
Hence the first 12 terms will be:

F1 = 1
F2 = 1
F3 = 2
F4 = 3
F5 = 5
F6 = 8
F7 = 13
F8 = 21
F9 = 34
F10 = 55
F11 = 89
F12 = 144
The 12th term, F12, is the first term to contain three digits.

What is the first term in the Fibonacci sequence to contain 1000 digits?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import math
s5 = 5 ** 0.5
logp = math.log(0.5 * (1 + s5))
log10 = math.log(10)

def first_fib(digits):
    '''Return the index of the first term in the Fibonacci sequence to contain ''digits'' digits.
    digits >= 2.
    
    >>> first_fib(2)
    7

    >>> first_fib(3)
    12

    >>> first_fib(1000)
    4782
    '''
    d = digits - 1
    return int(math.ceil((log10 * d + math.log(s5 + 0.5 * 10 ** (-d))) / logp))  

if __name__ == "__main__":
    import doctest
    doctest.testmod()
