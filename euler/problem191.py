'''
============================================================
http://projecteuler.net/problem=191

A particular school offers cash rewards to children with good attendance and punctuality. If they are absent for three consecutive days or late on more than one occasion then they forfeit their prize.

During an n-day period a trinary string is formed for each child consisting of L's (late), O's (on time), and A's (absent).

Although there are eighty-one trinary strings for a 4-day period that can be formed, exactly forty-three strings would lead to a prize:

OOOO OOOA OOOL OOAO OOAA OOAL OOLO OOLA OAOO OAOA
OAOL OAAO OAAL OALO OALA OLOO OLOA OLAO OLAA AOOO
AOOA AOOL AOAO AOAA AOAL AOLO AOLA AAOO AAOA AAOL
AALO AALA ALOO ALOA ALAO ALAA LOOO LOOA LOAO LOAA
LAOO LAOA LAAO

How many "prize" strings exist over a 30-day period?
============================================================
'''
import numpy as np
from itertools import product

def extend_counts(x):  # y=Ax
    y = np.zeros_like(x)
    for l, k in product(xrange(3), xrange(2)):
        for m in xrange(3 if k == 0 else 4):
            xc = x[l, k, m]
            y[l, k, 0] += xc
            y[min(2, l + 1), k, 0] += xc
            y[l, (k + 1) if k == 0 and m == 2 else k, min(3, m + 1)] += xc
    return y

def initial_counts():
    x = np.zeros((3, 2, 4), dtype=np.long)
    x[0, 0, 0] = x[0, 0, 1] = x[1, 0, 0] = 1
    return x

def num_prize_strings(n):
    x = initial_counts()
    for _ in xrange(n - 1): x = extend_counts(x)
    return sum(x[:2, 0, :].flatten())

if __name__ == "__main__":
    print num_prize_strings(4)
    print num_prize_strings(30)
