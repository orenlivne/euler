'''
============================================================
http://projecteuler.net/problem56

A googol (10100) is a massive number: one followed by one-hundred zeros; 100100 is almost unimaginably large: one followed by two-hundred zeros. Despite their size, the sum of the digits in each number is only 1.

Considering natural numbers of the form, ab, where a, b  100, what is the maximum digital sum?
============================================================
'''

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    import time

    start = time.time()
    print max(sum(map(int, str(a ** b))) for a in xrange(2, 100) for b in xrange(1, 100))
    print time.time() - start, 'sec'

    start = time.time()
    print max(sum(map(int, str(a ** b))) for a in xrange(90, 100) for b in xrange(90, 100))
    print time.time() - start, 'sec'
