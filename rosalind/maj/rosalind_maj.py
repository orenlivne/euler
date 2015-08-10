'''
============================================================
http://rosalind.info/problems/maj

An array A[1..n] is said to have a majority element if more than half of its entries are the same.

Given: A positive integer k<=20, a positive integer n<=104, and k arrays of size n containing positive integers not exceeding 105.

Return: For each array, output an element of this array occurring strictly more than n/2 times if such element exists, and "-1" otherwise.

Source: Algorithms by Dasgupta, Papadimitriou, Vazirani. McGraw-Hill. 2006.
============================================================
'''
from collections import Counter
import itertools as it
import rosalind.rosutil as ro

def majority_element(a):
    return (lambda x: x[1] if x[0] > len(a) / 2 else -1)(max((v, k) for k, v in Counter(a).iteritems()))

def solve_maj(f):
    return ro.join_list(it.imap(majority_element, it.imap(ro.to_int_list, ro.skip(ro.iterlines(f), 1))))

if __name__ == "__main__":
#    print solve_maj('rosalind_maj_sample.dat')
    print solve_maj('rosalind_maj.dat')
