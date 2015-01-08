'''
============================================================
http://projecteuler.net/problem=93

By using each of the digits from the set, {1, 2, 3, 4}, exactly once, and making use of the four arithmetic operations (+, , *, /) and brackets/parentheses, it is possible to form different positive integer targets.

For example,

8 = (4 * (1 + 3)) / 2
14 = 4 * (3 + 1 / 2)
19 = 4 * (2 + 3)  1
36 = 3 * 4 * (2 + 1)

Note that concatenations of the digits, like 12 + 34, are not allowed.

Using the set, {1, 2, 3, 4}, it is possible to obtain thirty-one different target numbers of which 36 is the maximum, and each of the numbers 1 to 28 can be obtained before encountering the first non-expressible number.

Find the set of four distinct digits, a < b < c < d, for which the longest set of consecutive positive integers, 1 to n, can be obtained, giving your answer as a string: abcd.
============================================================
'''
from __future__ import division
import itertools as it
L, R = '(', ')'

def forms(operands, operations):
    '''All expressions that can be formed from the operands and operations. Both arguments are 
    string lists.'''
    a, b, c, d = operands
    o1, o2, o3 = operations
    return [a + o1 + b + o2 + c + o3 + d,
            L + a + o1 + b + R + o2 + c + o3 + d,
            L + a + o1 + b + R + o2 + L + c + o3 + d + R,
            L + a + o1 + b + o2 + c + R + o3 + d,
            L + L + a + o1 + b + R + o2 + c + R + o3 + d,
            L + a + o1 + L + b + o2 + c + R + R + o3 + d,
            a + o1 + L + b + o2 + c + R + o3 + d,
            a + o1 + L + b + o2 + c + o3 + d + R,
            a + o1 + L + L + b + o2 + c + R + o3 + d + R,
            a + o1 + L + b + o2 + L + c + o3 + d + R + R,
            a + o1 + b + o2 + L + c + o3 + d + R] 
    
def eval_safe(s):
    try: return eval(s)
    except ZeroDivisionError: return 0
     
def max_seq():
    n_max = -1
    for operands in it.combinations(map(str, xrange(1, 10)), 4):
        f = set([])
        for perm_operands, operations in it.product(it.permutations(operands), it.product('+-*/', repeat=3)):
            f |= set(map(int, filter(lambda x: x > 0 and x - int(x) < 1e-12, map(eval_safe, forms(perm_operands, operations)))))
        try:
            n = it.dropwhile(lambda x: x[0] == x[1], enumerate(f, 1)).next()[0] - 1 if f else 0
        except StopIteration:
            n = len(f)
        print ''.join(operands),n
        #print '\t\t', n#, f_all
        if n > n_max: n_max, digits = n, ''.join(operands)
    return digits

if __name__ == "__main__":
    print max_seq()
