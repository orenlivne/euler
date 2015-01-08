'''
============================================================
http://projecteuler.net/problem=65

The square root of 2 can be written as an infinite continued fraction.

The infinite continued fraction can be written, 2 = [1;(2)], (2) indicates that 2 repeats ad infinitum. In a similar way, 23 = [4;(1,3,1,8)].

It turns out that the sequence of partial values of continued fractions for square roots provide the best rational approximations. Let us consider the convergents for 2.

Hence the sequence of the first ten convergents for 2 are:

1, 3/2, 7/5, 17/12, 41/29, 99/70, 239/169, 577/408, 1393/985, 3363/2378, ...
What is most surprising is that the important mathematical constant,
e = [2; 1,2,1, 1,4,1, 1,6,1 , ... , 1,2k,1, ...].

The first ten terms in the sequence of convergents for e are:

2, 3, 8/3, 11/4, 19/7, 87/32, 106/39, 193/71, 1264/465, 1457/536, ...
The sum of digits in the numerator of the 10th convergent is 1+4+5+7=17.

Find the sum of digits in the numerator of the 100th convergent of the continued fraction for e.
============================================================
'''
import itertools as it

e_expansion = lambda n: 2 if n == 0 else (2 * (n / 3 + 1) if n % 3 == 2 else 1)

def cont_convergent(a):
    '''Yield (h,k), where h/k are convergents of the continued fraction whose coefficients are
    are given by the iterate a.'''
    h0, h1 = (0, 1), (1, 0)
    while True:
        an = a.next()
        h2 = (an * h1[0] + h0[0], an * h1[1] + h0[1])
        yield h2
        h0, h1 = h1, h2
        
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print sum(it.imap(int, str(it.islice(cont_convergent(it.imap(e_expansion, it.count())), 99, 100).next()[0])))
