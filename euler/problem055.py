'''
============================================================
http://projecteuler.net/problem=55

If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,

349 + 943 = 1292,
1292 + 2921 = 4213
4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome. A number that never forms a palindrome through the reverse and add process is called a Lychrel number. Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that a number is Lychrel until proven otherwise. In addition you are given that for every number below ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome. In fact, 10677 is the first number to be shown to require over fifty iterations before producing a palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.

How many Lychrel numbers are there below ten-thousand?

NOTE: Wording was modified slightly on 24 April 2007 to emphasise the theoretical nature of Lychrel numbers.
============================================================
'''
import timeit

#-------------------------------------------------------------------------
reverse = lambda x: int(''.join(reversed(str(x))))

def is_lychrel(x, max_iter):
    for i in xrange(max_iter):
        y = reverse(x)
        if i > 0 and x == y:
            return False
        x += y
    return True
        
a = lambda : sum(1 for x in xrange(10000) if is_lychrel(x, 50))

#-------------------------------------------------------------------------
def is_lychrel3(x, max_iter):
    y = reverse(x)
    x += y
    for _ in xrange(max_iter - 1):
        y = reverse(x)
        if x == y:
            return False
        x += y
    return True

a3 = lambda : sum(1 for x in xrange(10000) if is_lychrel3(x, 50))

#-------------------------------------------------------------------------
# pokop solution 29-MAR-13. A bit slower than ours. 
# def reverse2(n):
#     x = 0
#     while n > 0:
#         x = x * 10 + n % 10
#         n /= 10
#     return x
# 
# def is_lychrel2(n):
#     r = reverse(n)
#     for _ in xrange(50):
#         n += r
#         r = reverse(n)
#         if n == r:
#             return False
#     return True
#    
# a2 = lambda : sum((1 for i in xrange(1, 10 ** 4) if is_lychrel2(i)))

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    num_calls = 10
    print timeit.timeit('a3()', 'from __main__ import is_lychrel3, a3', number=num_calls) / num_calls
    print timeit.timeit('a()', 'from __main__ import is_lychrel, a', number=num_calls) / num_calls
    # print timeit.timeit('a2()', 'from __main__ import is_lychrel2, a2', number=num_calls) / num_calls
