'''
============================================================
http://projecteuler.net/problem=48

The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
============================================================
'''
def sum_right_digits(n, k):
    '''Last k digits of sum(i^i, i=1..n).'''
    p = 10 ** k
    return reduce(lambda x, y: (x + y) % p, (pow_mod_p(x, p) for x in xrange(1, n + 1)))

def pow_mod_p(x, p):
    '''x^x mod p, x >= 0.'''
    d, y = x, 1  # d holds x^(2^k) mod p, k=1,2,...; y holds the result
    #print list(reversed(map(int, str(bin(x)[2:]))))
    for b in reversed(map(int, str(bin(x)[2:]))):
        #print b, d, x, y
        if b:
            y = (y * d) % p
        d = (d * d) % p
    #print d
    return y
    
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    #print [pow_mod_p(x, 100) for x in xrange(10)]
    print sum_right_digits(1000, 10)
    
