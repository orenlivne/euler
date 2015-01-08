'''
============================================================
http://projecteuler.net/problem=31

In England the currency is made up of pound, E, and pence, p, and there are eight coins in
general circulation:

1p, 2p, 5p, 10p, 20p, 50p, E1 (100p) and E2 (200p).
It is possible to make E2 in the following way:

1E1 + 150p + 220p + 15p + 12p + 31p
How many different ways can E2 be made using any number of coins?
============================================================
'''
class CurrencyCombo(object):
    '''Currency combination calculator.'''
    def __init__(self, b):
        ''''b = list of coin values. Must consist of positive integers.'''
        self._b = sorted(b)
        self._p = {}        # Cache of p-values. If class is reused many times, replace with a weak hash map to manage its size
        
    def _ways(self, k, x):
        '''Returns #ways to make the amount x with the k smallest coins.'''
        return self._p.setdefault((k, x), self._calc_ways(k, x))
    
    def ways(self, x):
        '''Returns #ways to make the amount x with all available coins.'''
        return self._ways(len(self._b), x)
    
    def _calc_ways(self, k, x):
        '''A helper function to calculate P[k,x] when it is not in the cache yet.'''
        if x == 0 or k == 0:
            # Empty amount or no coins ==> can't make it
            return 0
        else:
            km = k - 1
            b = self._b[km]
            return sum(self._ways(km, x - i * b) for i in xrange(x / b + 1)) + (1 if (x % b == 0) else 0)

def ways_bottom_up(b, x):
    '''Bottom-up dynamic programming approach. Both more time- and space- efficient than the top-down
    approach in CurrencyCombo.'''
    p = [1] + [0] * x
    for c in sorted(b):
        for y in xrange(c, x + 1):
            p[y] += p[y - c]
    return p[x] 

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    import timeit
    
    print ways_bottom_up([1, 2, 5, 10, 20, 50, 100, 200], 200)
    print ways_bottom_up([1, 2, 5, 10, 20, 50, 100, 200], 10000)

    n = 100
    print timeit.timeit('problem031.ways_bottom_up([1, 2, 5, 10, 20, 50, 100, 200], 200)', setup='import problem031', number=n) / n
    n = 1
    print timeit.timeit('c.ways(200)', setup='import problem031; c = problem031.CurrencyCombo([1, 2, 5, 10, 20, 50, 100, 200])', number=n) / n

    #c = CurrencyCombo([1, 2, 5, 10, 20, 50, 100, 200])
    #print c.ways(200)
    
