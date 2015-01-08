'''
============================================================
http://projecteuler.net/problem=120

Let r be the remainder when (a1)n + (a+1)n is divided by a2.

For example, if a = 7 and n = 3, then r = 42: 63 + 83 = 728  42 mod 49. And as n varies, so too will r, but for a = 7 it turns out that rmax = 42.

For 3  a  1000, find sum rmax.
============================================================
'''
s1 = lambda n: n * (n + 1) / 2
s2 = lambda n: n * (n + 1) * (2 * n + 1) / 6

# def rmax(a):
#    a2 = a * a
#    print [(2 if n % 2 == 0 else (2 * n * a) % a2) for n in xrange(1, 2 * (a / 2 if a % 2 == 0 else a) + 1, 2)]
#    return max((2 if n % 2 == 0 else (2 * n * a) % a2) for n in xrange(1, 2 * (a / 2 if a % 2 == 0 else a) + 1, 2))
rmax = lambda a: a * (a - 2) if a % 2 == 0  else a * (a - 1) # hv's comment

if __name__ == "__main__":
    print sum(rmax(a) for a in xrange(3, 1001))
