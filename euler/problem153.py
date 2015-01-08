'''
============================================================
http://projecteuler.net/problem=153

As we all know the equation x2=-1 has no solutions for real x. 
If we however introduce the imaginary number i this equation has two solutions: x=i and x=-i. 
If we go a step further the equation (x-3)2=-4 has two complex solutions: x=3+2i and x=3-2i. 
x=3+2i and x=3-2i are called each others' complex conjugate. 
Numbers of the form a+bi are called complex numbers. 
In general a+bi and a-bi are each other's complex conjugate.

A Gaussian Integer is a complex number a+bi such that both a and b are integers. 
The regular integers are also Gaussian integers (with b=0). 
To distinguish them from Gaussian integers with b != 0 we call such integers "rational integers." 
A Gaussian integer is called a divisor of a rational integer n if the result is also a Gaussian integer. 
If for example we divide 5 by 1+2i we can simplify  in the following manner: 
Multiply numerator and denominator by the complex conjugate of 1+2i: 1-2i. 
The result is  . 
So 1+2i is a divisor of 5. 
Note that 1+i is not a divisor of 5 because . 
Note also that if the Gaussian Integer (a+bi) is a divisor of a rational integer n, then its complex conjugate (a-bi) is also a divisor of n.

In fact, 5 has six divisors such that the real part is positive: {1, 1 + 2i, 1 - 2i, 2 + i, 2 - i, 5}. 
The following is a table of all of the divisors for the first five positive rational integers:

n     Gaussian integer divisors
with positive real part    Sum s(n) of 
these divisors
1    1    1
2    1, 1+i, 1-i, 2    5
3    1, 3    4
4    1, 1+i, 1-i, 2, 2+2i, 2-2i,4    13
5    1, 1+2i, 1-2i, 2+i, 2-i, 5    12
For divisors with positive real parts, then, we have: .

For 1 <= n <= 105, SUM s(n)=17924657155.

What is SUM s(n) for 1 <= n <= 10**8?
============================================================
'''
from problem005 import gcd

#-------------------------------
# Real (rational) divisors
#-------------------------------
def sum_divisors_rational(n):
    '''Returns the sum of rational divisors of all numbers between 1 and n, inclusive. A fast
    implementation that decomposes the requested sum, sum_{a=1}^n a*floor(n/a) into local
    and smooth parts, because floor(n/.) becomes increasingly smoother for larger values of
    the argument. Runtime complexity: O(sqrt(n)).'''
    # Optimal split to balance local and smoth work
    q = int(n ** 0.5)
    # Local part
    s_local = sum(a * (n / a) for a in xrange(1L, n / q + 1))
    # Smooth part
    s_smooth = 0L
    for k in xrange(1L, q):
        r1, r2 = n / (k + 1), n / k
        # print '\t', r1, r2
        s_smooth += k * (r1 + r2 + 1) * (r2 - r1)
    s_smooth /= 2
    # print n, K, s_local, s_smooth
    
    return s_local + s_smooth

#-------------------------------
# Complex divisors
#-------------------------------
def g_sum(n, p):
    '''Return the inner-most sum of complex Gaussian divisors with positive real part of all k, k=1..n.
    Using a summation formula. Runtime complexity: O(n^(1/2)).'''
    # Optimal split to balance local and smoth work
    q, s = int((n / p) ** 0.5), 0L
    # Local part
    for g in xrange(1L, n / (p * q) + 1):
        K = n / (p * g)
        s += (K * g + K * (K + 1) / 2)
    # Smooth part
    for k in xrange(1L, q):
        r1, r2 = n / (p * (k + 1)), n / (p * k)
        G = (r1 + r2 + 1) * (r2 - r1) / 2
        s += (k * G + k * (k + 1) * (r2 - r1) / 2)
    return s

'''Return the sum of complex Gaussian divisors with positive real part of all k, k=1..n.
Using a summation formula. Runtime complexity: O(n).'''
sum_divisors_complex = lambda n: \
sum(a * sum(g_sum(n, a * a + b * b) for b in xrange(1, int((n - a * a) ** 0.5) + 1) if gcd(a, b) == 1)
    for a in xrange(1, int((n - 1) ** 0.5) + 1))

sum_divisors_gaussian = lambda n: sum_divisors_rational(n) + sum_divisors_complex(n)
 
if __name__ == "__main__":
    print sum_divisors_gaussian(10L ** 8)
