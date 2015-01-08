'''
============================================================
http://projecteuler.net/problem=169

Define f(0)=1 and f(n) to be the number of different ways n can be expressed as a sum of integer powers of 2 using each power no more than twice.

For example, f(10)=5 since there are five different ways to express 10:

1 + 1 + 8
1 + 1 + 4 + 4
1 + 1 + 2 + 2 + 4
2 + 4 + 4
2 + 8

What is f(1025)?
============================================================
'''
def f(n, m={}):
    if m.has_key(n): return m[n]
    return m.setdefault(n, _f(n, m))

_f = lambda n, m: 1 if n == 0 else (f(n / 2, m) if n % 2 else f(n / 2, m) + f(n / 2 - 1, m))
    
if __name__ == "__main__":
    print f(10)
    print f(10 ** 25)
