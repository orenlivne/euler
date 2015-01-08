'''
============================================================
http://projecteuler.net/problem=173

Problem 173
We shall define a square lamina to be a square outline with a square "hole" so that the shape possesses vertical and horizontal symmetry. For example, using exactly thirty-two square tiles we can form two different square laminae:

(a figure describing 32=9^2-7^2 =6^2-2^2)
 
With one-hundred tiles, and not necessarily using all of the tiles at one time, it is possible to form forty-one different square laminae.

Using up to one million tiles how many different square laminae can be formed?
============================================================
'''
import numpy as np

def num_laminae(N):
    '''Return the number of divisors c of n s.t. n=c*d, c<d, and c,d have same parity,
    for all 0 <= n <= N.'''
    d = np.zeros((N / 4 + 1,), dtype=np.int)  # Every n is divisible by 1
    for n in xrange(1, N / 4 + 1): d[n::n] += 1
    d[np.array([x * x for x in xrange(1, int(N ** 0.5) / 2 + 1)])] -= 1
    d /= 2
    return sum(d)

if __name__ == "__main__":
    print num_laminae(100)
    print num_laminae(10 ** 6)
