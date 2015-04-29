'''n people standing in a circle in an order 0 to n-1. No. 0 has a sword. He
kills the next person (i.e. No. 1) and gives the sword to the next (i.e. No.
3). All people do the same until only one survives. Find the number of the
person that survives.'''

def last_man_standing_using_list(n):
    '''O(n^2) implementation: O(log n) rounds, each of each touches each
    remaining element once (so, n + n/2 + n/4 + ... ~ 2n). But the look-up
    of ring[index] cost O(index).'''
    ring, index = range(n), 0
    while len(ring) > 1:
        index = (index + 1) % len(ring)
        ring.remove(ring[index])
    return ring[0]

def last_man_standing_using_recursion(n):
    '''Recursive implementation by Matthias Blume. O(n) time, O(n) stack
    size.'''
    return 0 if n <= 1 else (last_man_standing_using_recursion(n-1) + 2) % n

def last_man_standing_fast(n):
    '''Recursive implementation by Matthias Blume. O(log n) time & stack.'''
    if n <= 1: return 0
    l = last_man_standing_fast(n/2)
    if n % 2: l += 1
    return 2*l

def last_man_standing_formula(n):
    '''Closed-form formula: 2*(n - 2**[log2(n)]). O(log n) to evaluate.'''
    m, p = n, 1
    while m > 1:
        p <<= 1
        m >>= 1
    return (n - p) << 1


if __name__ == "__main__":
    for n in xrange(1, 101):
        print n, bin(n)[2:], last_man_standing_using_list(n), \
            last_man_standing_using_recursion(n), last_man_standing_fast(n), \
            last_man_standing_formula(n)
