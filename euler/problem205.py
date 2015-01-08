'''
============================================================
http://projecteuler.net/problem=206

Peter has nine four-sided (pyramidal) dice, each with faces numbered 1, 2, 3, 4.
Colin has six six-sided (cubic) dice, each with faces numbered 1, 2, 3, 4, 5, 6.

Peter and Colin roll their dice and compare totals: the highest total wins. The result is a draw if the totals are equal.

What is the probability that Pyramidal Pete beats Cubic Colin? Give your answer rounded to seven decimal places in the form 0.abcdefg
============================================================
'''
from numpy import cumsum

def F(s, n):
    '''Returns [Fs(n,n),...,Fs(n,s*n)] of probabilities to get dice sums n,...,s*n with n dice,
    each having s sides.'''
    if n == 1: return [1. / s] * s
    else:
        Fp = F(s, n - 1)
        return [sum(Fp[k - n:k - min(k - n + 1, s) - n:-1] if (k - min(k - n + 1, s) - n >= 0)
                    else  Fp[k - n::-1]) / float(s) for k in xrange(n, s * n + 1)]

p_winning = lambda s1, n1, s2, n2: sum(x * y for x, y in zip(F(s1, n1), cumsum(F(s2, n2))[n1 - n2 - 1:])) if n1 > n2 else sum(x * y for x, y in zip(F(s1, n1)[n2 - n1 + 1:], cumsum(F(s2, n2)))) 
p_draw = lambda s1, n1, s2, n2: sum(x * y for x, y in zip(F(s1, n1), F(s2, n2)[n1 - n2:])) if n1 > n2 else sum(x * y for x, y in zip(F(s1, n1)[n2 - n1:], F(s2, n2))) 

if __name__ == "__main__":
    print '%.7f %.7f %.7f' % (p_winning(4, 9, 6, 6), p_draw(6, 6, 4, 9), p_winning(6, 6, 4, 9))
    print '%.7f %.7f %.7f' % (p_winning(2, 18, 6, 6), p_draw(6, 6, 2, 18), p_winning(6, 6, 2, 18))
