'''
============================================================
http://projecteuler.net/problem=74

The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:

1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to 169; it turns out that there are only three such loops that exist:

169  363601  1454  169
871  45361  871
872  45362  872

It is not difficult to prove that EVERY starting number will eventually get stuck in a loop. For example,

69  363600  1454  169  363601 ( 1454)
78  45360  871  45361 ( 871)
540  145 ( 145)

Starting with 69 produces a chain of five non-repeating terms, but the longest non-repeating chain with a starting number below one million is sixty terms.

How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?
============================================================
'''
import numpy as np, itertools as it

'''Lookup table for digit factorials'''
DIGIT_FAC = np.concatenate(([1], np.cumprod(xrange(1, 10))))
                           
# The iteration
digit_fac_iteration = lambda x: sum(map(DIGIT_FAC.__getitem__, map(int, str(x))))                        
# List of all cycles of length > 1 in the iteration of interest
cycles = [(169, 363601, 1454), (871, 45361), (872, 45362)]

'''All permutations of a number x that are less than n.'''
perms = lambda x, n : np.array([0]) if x == 0 else np.array(filter(lambda y: y < n, map(int, (''.join(y) for y in it.permutations(str(x)) if y[0] != '0'))))

def cycle_length(iteration, n, cycles=[]):
    '''Return an array of the number of non-repeating terms in the iteration ''iteration'', 
    starting from any number between 0 and n-1, and given a comprehensive list of cycles of
    length > 1 ''cycles''.'''
    c, x, s, sz = np.zeros((n,), dtype=np.uint), 0, [], n  # c[i] = cycle length starting from i
    for cycle in cycles: c[np.array(cycle)] = len(cycle)  # Initial conditions
    while x < n:
        if x % 10000 == 0:
            print 'x', x
        # Push x's iterates on stack s until we arrive at an already-computed cycle length
        # (c[y]>0) 
        y = x
        while not c[y]:
            s.append(y)
            z = iteration(y)
            # print '\t', 'z', z
            if z == y:
                y_perms = perms(y, sz)
                max_perm = y_perms[-1]  # perms are sorted
                if max_perm >= sz:
                    sz = max(int(1.5 * sz), max_perm)
                    c = np.resize(c, sz)
                c[y_perms] = 1
                s.pop()
                break
            y = z
            if y >= sz:
                sz = int(1.5 * sz)
                c = np.resize(c, sz)
        
        # Pop elements from stack and set their cycle index ((dynamic programming)
        l = c[y]
        while s:
            l += 1
            y_perms = perms(s.pop(), sz)  # perms are sorted
            max_perm = y_perms[-1]
            if max_perm >= sz:
                sz = max(int(1.5 * sz), max_perm)
                c = np.resize(c, sz)
            c[y_perms] = l
    
        # Advance pointer to next non-computed number
        while x < n and c[x]: x += 1
    return c[:n]

if __name__ == "__main__":
    import time
    start = time.time()
    c = cycle_length(digit_fac_iteration, 1000000, cycles)
    print time.time() - start
    print len(np.where(c == 60)[0])
