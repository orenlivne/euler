'''
============================================================
http://projecteuler.net/problem=145

Some positive integers n have the property that the sum [ n + reverse(n) ] consists entirely of odd (decimal) digits. For instance, 36 + 63 = 99 and 409 + 904 = 1313. We will call such numbers reversible; so 36, 63, 409, and 904 are reversible. Leading zeroes are not allowed in either n or reverse(n).
There are 120 reversible numbers below one-thousand.
How many reversible numbers are there below one-billion (109)?
============================================================
'''
from numpy import prod, abs

class ReversibleCounter(object):
    '''Counts d-digit reversible numbers.'''
    def __init__(self, d):
        self.d2 = (d + 1) / 2
        self.odd_d = d % 2
        self.t = [10 ** k + 10 ** (d - 1 - k) for k in xrange(self.d2)]
        self.max_x = 2 * 10 ** d
        
    def count(self): return self._count([0] * self.d2, 0, 0)
    
    def _count(self, b, x, k):
        if k == self.d2: return self._count_at_leaf(b, x)
        # Sum over all branches in which the value of b[k] satisfies the kth constraint (that the
        # kth digit of x is odd)
        b_copy, tk, count = list(b), self.t[k], 0
        for bk in xrange(1 if (k == 0) else 0, 10 if (self.odd_d and k == self.d2 - 1) else 18):
            y = x + tk * bk
            ys = str(y)
            if y < self.max_x and int(ys[len(ys) - 1 - k]) % 2 == 1:
                b_copy[k] = bk
                count += self._count(b_copy, y, k + 1)
        return count

    def _count_at_leaf(self, b, x):
        xs = str(x)
        count = prod([1 if self.odd_d and k == self.d2 - 1 else
                      (9 - abs(c - 10) if k == 0 else 10 - abs(c - 9))
                      for k, c in enumerate(b)]) if \
            all(int(xs[k]) % 2 == 1 for k in xrange(self.d2 + 1)) else 0
        return count
    
reversible_count = lambda max_d: sum(ReversibleCounter(d).count() for d in xrange(1, max_d + 1))

if __name__ == "__main__":
    print reversible_count(3)
    print reversible_count(9)
