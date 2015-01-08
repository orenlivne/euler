'''
============================================================
http://projecteuler.net/problem=277

A modified Collatz sequence of integers is obtained from a starting value a1 in the following way:

an+1 = an/3 if an is divisible by 3. We shall denote this as a large downward step, "D".

an+1 = (4an + 2)/3 if an divided by 3 gives a remainder of 1. We shall denote this as an upward step, "U".

an+1 = (2an - 1)/3 if an divided by 3 gives a remainder of 2. We shall denote this as a small downward step, "d".

The sequence terminates when some an = 1.

Given any integer, we can list out the sequence of steps.
For instance if a1=231, then the sequence {an}={231,77,51,17,11,7,10,14,9,3,1} corresponds to the steps "DdDddUUdDD".

Of course, there are other sequences that begin with that same sequence "DdDddUUdDD....".
For instance, if a1=1004064, then the sequence is DdDddUUdDDDdUDUUUdDdUUDDDUdDD.
In fact, 1004064 is the smallest possible a1 > 106 that begins with the sequence DdDddUUdDD.

What is the smallest a1 > 1015 that begins with the sequence "UDDDUdddDDUDDddDdDddDDUDDdUUDd"?
============================================================
'''
from problem134 import extended_gcd
from problem234 import int_ceil

def smallest_collatz(seq, L):
    '''Return the smallest starting number > L for the modified Collatz sequence starting with
    the encoded move sequence seq.''' 
    r, two_k, n3 = 0L, 1L, pow(3L, len(seq))
    # The reverse Collatz sequence has the form b_n = (3*n b_0 + r_n)/2^(k_n). r_n, 2^(k_n) admit an
    # easy recurrence relationship vs. r_(n-1), 2^(k_(n-1)).
    for move in reversed(seq):
        if move == 'D': r *= 3
        elif move == 'U': r, two_k = 3 * r - 2 * two_k, 4 * two_k
        elif move == 'd': r, two_k = 3 * r + two_k, 2 * two_k
    # Use the Chinese remainder theorem to derive the form b_n = 3^n x + a*r where a = multiplicative
    # inverse of 2^(k_n) mod 3^n. a is efficiently found using the extended Euclid algorithm. Convert
    # this to b_n = 3^n + R where 0 <= R < 3^n.
    R = extended_gcd(two_k, n3)[0] * r % n3
    return n3 * int_ceil((L + 1. - R) / n3) + R
    
if __name__ == "__main__":
    print smallest_collatz('DdDddUUdDD', pow(10L, 6))
    print smallest_collatz('UDDDUdddDDUDDddDdDddDDUDDdUUDd', pow(10L, 15))
