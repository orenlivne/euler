'''
============================================================
http://projecteuler.net/problem=188

The hyperexponentiation or tetration of a number a by a positive integer b, denoted by a||b or ba, is recursively defined by:

a||1 = a,
a||(k+1) = a(a||k).

Thus we have e.g. 3||2 = 33 = 27, hence 3||3 = 327 = 7625597484987 and 3||4 is roughly 103.6383346400240996*10^12.

Find the last 8 digits of 1777||1855.
============================================================
'''
def fmod(a, k, n):  # Works if a**n (mod n) = 1
    f = a
    for _ in xrange(k - 1): f = pow(a, f, n)
    return f

if __name__ == "__main__":
    print fmod(1777, 1855, 10 ** 8)
