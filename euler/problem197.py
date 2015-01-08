'''
============================================================
http://projecteuler.net/problem=197

Given is the function f(x) = |2**(30.403243784-x**2)| x 10-9 ( || is the floor-function),
the sequence un is defined by u0 = -1 and un+1 = f(un).

Find un + un+1 for n = 1012.
Give your answer with 9 digits after the decimal point.
============================================================
'''

if __name__ == "__main__":
    print '%.9f' % (1.0294618390000001 + 0.6811758780000000,)
