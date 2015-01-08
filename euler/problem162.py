'''
============================================================
http://projecteuler.net/problem=162

In the hexadecimal number system numbers are represented using 16 different digits:

0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F
The hexadecimal number AF when written in the decimal number system equals 10x16+15=175.

In the 3-digit hexadecimal numbers 10A, 1A0, A10, and A01 the digits 0,1 and A are all present.
Like numbers written in base ten we write hexadecimal numbers without leading zeroes.

How many hexadecimal numbers containing at most sixteen hexadecimal digits exist with all of the digits 0,1, and A present at least once?
Give your answer as a hexadecimal number.

(A,B,C,D,E and F in upper case, without any leading or trailing code that marks the number as hexadecimal and without leading zeroes , e.g. 1A3F and not: 1a3f and not 0x1a3f and not $1A3F and not #1A3F and not 0000001A3F)
============================================================
'''
import numpy as np

def initial_counts(b):
    x = np.zeros((2, 2, 2), dtype=np.long)
    x[0, 1, 0] = x[0, 0, 1] = 1
    x[0, 0, 0] = b - 3
    return x
    
def extend_counts(x, b):
    y, b3 = np.zeros_like(x, dtype=np.long), b - 3
    for i in xrange(2):
        for j in xrange(2):
            for k in xrange(2):
                xc = x[i, j, k]
                y[min(1, i + 1), j, k] += xc
                y[i, min(1, j + 1), k] += xc
                y[i, j, min(1, k + 1)] += xc
                y[i, j, k] += b3 * xc
    return y

def num_3_present(N, b):
    x = initial_counts(b)
    s = x[1, 1, 1]
    for _ in xrange(2, N + 1):
        x = extend_counts(x, b)
        s += x[1, 1, 1]
    return s

remove_L = lambda x: x[:-1] if x[-1] == 'L' else x
num_3_present_hex = lambda N: remove_L(hex(num_3_present(N, 16))[2:].upper())

if __name__ == "__main__":
    print num_3_present_hex(16)
