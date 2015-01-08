'''
============================================================
http://projecteuler.net/problem=88

A natural number, N, that can be written as the sum and product of a given set of at least two natural numbers, {a1, a2, ... , ak} is called a product-sum number: N = a1 + a2 + ... + ak = a1  a2  ...  ak.

For example, 6 = 1 + 2 + 3 = 1  2  3.

For a given set of size, k, we shall call the smallest N with this property a minimal product-sum number. The minimal product-sum numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.

k=2: 4 = 2  2 = 2 + 2
k=3: 6 = 1  2  3 = 1 + 2 + 3
k=4: 8 = 1  1  2  4 = 1 + 1 + 2 + 4
k=5: 8 = 1  1  2  2  2 = 1 + 1 + 2 + 2 + 2
k=6: 12 = 1  1  1  1  2  6 = 1 + 1 + 1 + 1 + 2 + 6

Hence for 2k6, the sum of all the minimal product-sum numbers is 4+6+8+12 = 30; note that 8 is only counted once in the sum.

In fact, as the complete set of minimal product-sum numbers for 2k12 is {4, 6, 8, 12, 15, 16}, the sum is 61.

What is the sum of all the minimal product-sum numbers for 2k12000?
============================================================
'''
#---------------------- No queue storage, cache partial sums and products ----------------------
import numpy as np

def factors(max_value, max_size):
    '''A generator of non-decreasing factor sequences and their corresponding sums and products:
    ([2,2],4,4), ([2,3],5,6), ... 3-factors combos ... 4-factor combos... (up to max_size factors,
    whose maximum value is max_value)'''
    c, f = int(np.log2(max_value)), np.array([2, 2])
    i, s, p = len(f), np.cumsum(f), np.cumprod(f)
    while i <= c:
        yield f, s[-1], p[-1]
        j = i - 1  # Pointer to currently-incremented f-element
        while j >= 0:
            f[j] += 1  # Try to increment j. Update cumulative sum, product arrays
            f[j + 1:] = f[j]
            s[j], p[j] = f[0] if j == 0 else s[j - 1] + f[j], f[0] if j == 0 else p[j - 1] * f[j]
            for l in xrange(j + 1, i): s[l], p[l] = s[l - 1] + f[l], p[l - 1] * f[l]
            if p[-1] <= max_value: break  # Found a legal increment
            j -= 1
        if j < 0:  # Cannot further increment elements, increment sequence length
            i += 1
            f = np.tile(2, i) 
            s, p = np.cumsum(f), np.cumprod(f)

def sum_min_sum_product(N):
    '''Return the sum of all distinct minimal sum-product numbers for n terms.'''
    a_min = [2 * k for k in xrange(N + 1)]
    for f, s, a in factors(2 * N, int(np.log2(2 * N))):
        k = a - s + len(f)
        if k <= N and a < a_min[k]: a_min[k] = a
    return sum(set(a_min[2:]))

if __name__ == "__main__":
    print sum_min_sum_product(6)  # 30
    print sum_min_sum_product(12)  # 61
    print sum_min_sum_product(12000)  # 7587457

# from numpy import prod
# from math import log
# 
# #---------------------- SLOW AND WRONG ----------------------
# def min_sum_product_oren(n):
#     '''Return the minimal sum-product number for n terms.'''
#     a_min, z_min, c, search = 2 * n + 1, [], int(log(n) / log(2)) + 1, [[]]
#     num_ones = n - c
#     # print 'n', n, 'c', c
#     while search:
#         z = search.pop()
#         i = len(z)
#         # print z, i
#         if i == c:  # Full sequence, check if a solution
#             a = prod(z)
#             if a == sum(z) + num_ones and a < a_min: a_min, z_min = a, z
#         else:  # Partial sequence, append alternatives (DFS)
#             for zi in xrange(int((a_min / prod(z)) ** (1.0 / (c - i))), (1 if i == 0 else z[i - 1]) - 1, -1):
#                 search.append(z + [zi])
#     print 'n', n, 'a_min', a_min, z_min
#     return a_min
# 
# '''Return the sum of min sum-product numbers for #terms 2..N.''' 
# sum_min_sum_product_oren = lambda N: sum(set(map(min_sum_product_oren, xrange(2, N + 1))))
# 
# #---------------------- http://www.mathblog.dk/project-euler-88-minimal-product-sum-numbers/ ----------------------
# def sum_min_sum_product2(N):
#     a_min, c, N2 = [2 * k for k in xrange(N + 1)], int(log(2 * N) / log(2)), 2 * N
#     factors = [(x, y) for x in xrange(2, int(N2 ** 0.5) + 1) for y in xrange(x, N2 / x + 1)]
#     # num_factors = 1
#     count = 0
#     while factors:
#         # Pop from beginning of stack
#         z = factors.pop(0)
#         a, i = prod(z), len(z)
#         k = a - sum(z) + i
#         if k <= N and a < a_min[k]: a_min[k] = a
#         if i < c:
#             for zi in xrange(z[-1], N2 / a + 1): factors.append(z + (zi,))
#         count += 1
#         if count % 10000 == 0: print z, len(factors), a_min[:10]
#         # print z, a, k, factors, a_min
#     return sum(set(a_min[2:]))
