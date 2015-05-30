'''
============================================================
Given a+b and a XOR b, what is the number of distinct
ordered pairs (a,b) of positive integers?

If there are solutions, every 1-bit in x multiplies their number by 2 (a can be 0 and b can be 1
at that bit or vice versa, while their sum remains the same). Every 0-bit contributes one
solution (the a- and b- bit are the same, so swapping them gives the same numbers). So the number
of solutions is the number of 2^(1-bits in x).

Example:
s = 1010 = 10
x = 0100 = 4
a = A0BC (indeed, 0011 = 3)
b = A1BC (indeed, 0111 = 7)
OR
a = A1BC (indeed, 0111 = 7)
b = A0BC (indeed, 0011 = 3)
So there are two solutions: (3,7), (7,3), and their number is indeed 2^(#bits in x) = 2^1 = 2.

To determine if there are solutions, first fix all a's bits to 0 corresponding to x's 1-bits (as
we said, a's and b's bits can be swapped there, so without loss of generality, set all of a's to
0 and b's to 1). The rest are unknown. At x's 0-bits, b's bits equal a's bits. So adding a + b,
each unknown a-bit is left-shifted. We therefore verify that all bits of of s-x are covered by the
1-bits of 2*x.

Example:
s = 101110 = 78
x = 110000 = 48
So fix bits 4 and 5 in a to be 0. 
a = 00ABCD
b = 11ABCD
s = a + b = 2*D + 4*C + 8*B + 16*A + 16 + 32 = s
or s - x = 78 - 48 = 30 = 2*D + 4*C + 8*B + 16*A.
So                 s - x =  011110
Should equal                0ABCD0
Note that          2*x+1 = 1100001
AND get: (s-x) & (2*x+1) = 0000000 must be zero (otherwise we will have an s-x bit that's NOT
                                   covered by left-shifted 0-bits x)

Created on May 26, 2015
@author: Oren Livne <oren.livne@gmail.com>
============================================================
'''
def num_ones(x):
    # Returns the number of ones in the binary representation of x.
    count = 0
    while x: count, x = count + (x % 2), x / 2
    return count

def xor_pairs(s, x):
    # Returns the number of ordered pairs (a,b) with s = a + b and x = a ^ b. Complexity: O(log s).
    # Note: works even for x > s.
    return (1 << num_ones(x)) if ((s - x) & (2 * x + 1) == 0) else 0

def xor_pairs_brute_force(s, x):
    # Returns the number of ordered pairs (a, b) with s = a + b and x = a ^ b using brute force.
    # Complexity: O(s).
    return sum(1 for a in xrange(s + 1) if a ^ (s - a) == x)

def validate_vs_brute_force(max_s=1000):
    # Runs random testing of fast method against brute force and validate that the agree.
    for s in xrange(max_s + 1):
        print 'Testing with sum = %d ...' % (s,),
        for x in xrange(s + 2):  # a ^ b is a + b without carry, so x <= s. But cover a larger number as a corner case.
            assert(xor_pairs(s, x) == xor_pairs_brute_force(s, x))
        print ' OK'

if __name__ == '__main__':
    assert(xor_pairs_brute_force(10, 4) == 2)  # (3,7), (7,3)
    assert(xor_pairs(10, 4) == 2)  # (3,7), (7,3)
    assert(xor_pairs(100, 90) == 16)
    validate_vs_brute_force()
