'''
============================================================
http://projecteuler.net/problem=104

The Fibonacci sequence is defined by the recurrence relation:

Fn = Fn1 + Fn2, where F1 = 1 and F2 = 1.
It turns out that F541, which contains 113 digits, is the first Fibonacci number for which the last nine digits are 1-9 pandigital (contain all the digits 1 to 9, but not necessarily in order). And F2749, which contains 575 digits, is the first Fibonacci number for which the first nine digits are 1-9 pandigital.

Given that Fk is the first Fibonacci number for which the first nine digits AND the last nine digits are 1-9 pandigital, find k.
============================================================
'''
DIGITS = sorted(map(str, xrange(1, 10)))
is_pandigital = lambda s: sorted(s) == DIGITS

def smallest_fib_pan_index(f0=0, f1=1):
    p, n, f = 10 ** 9, 1, Fib(f0=f0, f1=f1)
    while True:
        n += 1
        f2 = (f0 + f1) % p
        if is_pandigital(str(f2)) and is_pandigital(str(f(n))[:9]): return n
        f0, f1 = f1, f2
    
class Fib(object):
    def __init__(self, f0=0, f1=1, r=None):
        if r: f0, f1 = f0 % r, f1 % r
        self.f, self.r = {0:f0, 1:f1}, r
    
    def __call__(self, n):
        if self.f.has_key(n): return self.f[n]
        else:
            if n % 2:
                x, y = self(n / 2), self(n / 2 + 1)
                result = x * x + y * y
            else:
                x, y = self(n / 2 - 1), self(n / 2)
                result = (2 * x + y) * y
            if self.r: result %= self.r
            return self.f.setdefault(n, result)
        
#---------------------------------------
import math
check = lambda number: set(str(number)) == set('123456789')

def smallest_fib_pan_index_Ra1nWarden():
    base1 = 1
    base2 = 1
    index = 3
    
    while True:
        number = (base1 + base2) % 1000000000
        if number > 100000000:
            if check(number):
                power = index * 0.20898764024997873 - 0.3494850021680094  # log10(F) ~ n*log10(phi) - log10(sqrt(5))
                leadnumber = int(math.pow(10, power + 8 - round(power, 0)))
                if check(leadnumber):
                    return index
        base1 = base2
        base2 = number
        index += 1
        
if __name__ == "__main__":
    print smallest_fib_pan_index_Ra1nWarden()
    print smallest_fib_pan_index()
    
