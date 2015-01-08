'''
============================================================
http://rosalind.info/problems/perm

Given: A positive integer n <= 7.

Return: The total number of permutations of length n, followed by a list of all such permutations (in any order).
============================================================
'''
from operator import mul
from rosalind.rosutil import read_ints_str

def lexperms(n):
    a, i = range(1, n + 1), n - 2  # Init first perm
    yield a
    if n == 1: return
    while True:
        ai, j = a[i], i + 1
        while j < n and a[j] > ai: j += 1  # j = max{k: k > i, a[k]>a[i]}
        j -= 1
        a[i], a[j] = a[j], a[i]  # Swap the ith and jth elements
        a[i + 1:] = a[:i:-1]  # Reverse the order
        yield a
        for i in xrange(n - 2, -1, -1):  # i = max{i: a[i] < a[i+1]}
            if a[i] < a[i + 1]: break
        if i == 0 and a[0] > a[1]: break  # perm is completely decreasing
    
perm = lambda n: repr(reduce(mul, xrange(1, n + 1))) + '\n' + '\n'.join(' '.join(map(str, a)) for a in lexperms(n))
    
if __name__ == "__main__":
    print perm(read_ints_str('rosalind_perm_sample.dat')[0])
    print perm(read_ints_str('rosalind_perm.dat')[0])
    
