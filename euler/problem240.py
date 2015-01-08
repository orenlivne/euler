'''
============================================================
http://projecteuler.net/problem=240

There are 1111 ways in which five 6-sided dice (sides numbered 1 to 6) can be rolled so that the top three sum to 15. Some examples are: 

D1,D2,D3,D4,D5 = 4,3,6,3,5 
D1,D2,D3,D4,D5 = 4,3,3,5,6 
D1,D2,D3,D4,D5 = 3,3,3,6,6 
D1,D2,D3,D4,D5 = 6,6,3,3,3 

In how many ways can twenty 12-sided dice (sides numbered 1 to 12) be rolled so that the top ten sum to 70?
============================================================
'''
from itertools import combinations_with_replacement
from euler.problem171 import C

'''Return the number of ways n s-sided dice can be rolled so that the top t sum up to x.'''
w = lambda n, s, t, x: sum(C(d) for d in combinations_with_replacement(xrange(1, s + 1), n) if sum(d[-t:]) == x)

if __name__ == "__main__":
    print w(5, 6, 3, 15) # 1111
    print w(20, 12, 10, 70) # 7448717393364181966
