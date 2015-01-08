'''
============================================================
http://projecteuler.net/problem=159

A composite number can be factored many different ways. For instance, not including multiplication by one, 24 can be factored in 7 distinct ways:

24 = 2x2x2x3
24 = 2x3x4
24 = 2x2x6
24 = 4x6
24 = 3x8
24 = 2x12
24 = 24
Recall that the digital root of a number, in base 10, is found by adding together the digits of that number, and repeating that process until a number is arrived at that is less than 10. Thus the digital root of 467 is 8.

We shall call a Digital Root Sum (DRS) the sum of the digital roots of the individual factors of our number.
The chart below demonstrates all of the DRS values for 24.

Factorisation    Digital Root Sum
2x2x2x3
9
2x3x4
9
2x2x6
10
4x6
10
3x8
11
2x12
5
24
6
The maximum Digital Root Sum of 24 is 11.
The function mdrs(n) gives the maximum Digital Root Sum of n. So mdrs(24)=11.
Find sum mdrs(n) for 1 < n < 1,000,000.
============================================================
'''
'''The digital root of n, except for n=1, where it is defined to be 0.'''
drs = lambda n: 0 if n == 1 else n - 9 * ((n - 1) / 9)

def mdrs(N):
    '''Return the Maximum Digital Root Sum (MDRS) of all n <= N. n=0,1 are defined to have MDRS=0.'''
    # 0th entry is not used. 1st entry is a boundary condition. Since it's 0, it does
    # Not affect the required MDRS sum.
    m = [0] * (N + 1)
    for d in xrange(2, N + 1):  # Loop over divisors of x
        drsd = drs(d)
        for k in xrange(1, N / d + 1):  # For all numbers n=k*d divisible by d ...
            n = k * d
            mn = drsd + m[k]
            if mn > m[n]:
                m[n] = mn
                for l in xrange(1, N / n + 1):
                    x = l * n
                    m[x] = max(m[x], drs(l) + mn)
    return m

if __name__ == "__main__":
    print sum(mdrs(10 ** 6 - 1))
