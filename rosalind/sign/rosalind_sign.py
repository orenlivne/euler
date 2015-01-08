'''
============================================================
http://rosalind.info/problems/sign

Given: A positive integer n<=6.
Return: The total number of signed permutations of length n, followed by a list of all such permutations (you may list the signed permutations in any order).
============================================================
'''
import rosalind.rosutil as ro, itertools as it, math

def sign(f):
    n = ro.read_int(f)
    print math.factorial(n) * 2 ** n
    for x in it.imap(lambda (x, y): tuple(x[i] * y[i] for i in xrange(len(x))), it.product(it.permutations(xrange(1, n + 1)), it.product(*((-1, 1) for _ in xrange(n))))): print ' '.join(map(str, x))

if __name__ == "__main__":
    #sign('rosalind_sign_sample.dat')
    sign('rosalind_sign.dat')
