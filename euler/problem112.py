'''
============================================================
http://projecteuler.net/problem=112
Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just over half of the numbers below one-thousand (525) are bouncy. In fact, the least number for which the proportion of bouncy numbers first reaches 50% is 538.

Surprisingly, bouncy numbers become more and more common and by the time we reach 21780 the proportion of bouncy numbers is equal to 90%.

Find the least number for which the proportion of bouncy numbers is exactly 99%.
============================================================
'''
import itertools as it

is_increasing_str = lambda x: all(x[k] <= x[k + 1] for k in xrange(len(x) - 1))
is_increasing = lambda x: is_increasing_str(str(x))
is_decreasing_str = lambda x: all(x[k] >= x[k + 1] for k in xrange(len(x) - 1))
is_decreasing = lambda x: is_decreasing_str(str(x))

def range_of_bouncy(t):
    '''Return the minimal N s.t. the portion of bouncy numbers <= N is >= t.'''
    b = 0  # A counter of bouncy numbers
    for x in it.count(1):
        if not is_increasing(x) and not is_decreasing(x):
            b += 1
        if b >= t * x:
            return x

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print range_of_bouncy(0.99)
