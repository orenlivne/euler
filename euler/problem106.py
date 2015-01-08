'''
============================================================
http://projecteuler.net/problem=106

Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:

S(B)  S(C); that is, sums of subsets cannot be equal.
If B contains more elements than C then S(B)  S(C).
For this problem we shall assume that a given set contains n strictly increasing elements and it already satisfies the second rule.

Surprisingly, out of the 25 possible subset pairs that can be obtained from a set for which n = 4, only 1 of these pairs need to be tested for equality (first rule). Similarly, when n = 7, only 70 out of the 966 subset pairs need to be tested.

For n = 12, how many of the 261625 subset pairs that can be obtained need to be tested for equality?

NOTE: This problem is related to problems 103 and 105.
============================================================
'''
import itertools as it

def disjoint_pairs(n):
    all_values = set(range(n))
    return ((x, y) for r in xrange(1, n + 1) 
            for x in it.combinations(xrange(n), r)
            for y in it.combinations(all_values - set(x), r) if x != y)

def valid_pairs(n):
    all_values = set(range(n))
    return ((x, y) for r in xrange(2, n / 2 + 1) 
            for x in it.combinations(xrange(n), r)
            for y in it.combinations(all_values - set(x), r)
            if x < y and not all(x[i] < y[i] for i in xrange(r)))
num_pairs = lambda n: (sum(1 for _ in valid_pairs(n)), sum(1 for _ in disjoint_pairs(n)))

if __name__ == "__main__":
    print num_pairs(4)  # 1
    print num_pairs(7)  # 70
    print num_pairs(12)  # 21384
    # print num_pairs(16)  # 1744847
    
