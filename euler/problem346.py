'''
============================================================
http://projecteuler.net/problem=346

The number 7 is special, because 7 is 111 written in base 2, and 11 written in base 6 
(i.e. 710 = 116 = 1112). In other words, 7 is a repunit in at least two bases b > 1.

We shall call a positive integer with this property a strong repunit. It can be verified that there are 8 strong repunits below 50: {1,7,13,15,21,31,40,43}. 
Furthermore, the sum of all strong repunits below 1000 equals 15864.

Find the sum of all strong repunits below 10**12.
============================================================
'''
def strong_repunits(N):
    '''Return the set of strong repunits < N.'''
    s = set([1])
    for b in xrange(2, int(((4 * N - 7) ** 0.5 - 1) * 0.5) + 1):
        x = b * b + b + 1
        while x < N:
            s.add(x)
            x = b * x + 1
    return s

if __name__ == "__main__":
    print sum(strong_repunits(10 ** 3)) # 15864
    print sum(strong_repunits(10 ** 12)) # 336108797689259276