'''
============================================================
http://projecteuler.net/problem=250

Find the number of non-empty subsets of {1**1, 2**2, 3**3,..., 250250**250250},
the sum of whose elements is divisible by 250. Enter the rightmost 16 digits as your answer.
============================================================
'''
def num_subsets(m, p, t):
    '''Return an array with the number of subsets (including the empty set) of {1**1,...,m**m}
    divisible by each r = 0,...,p-1. The output entries are subset numbers modulo t.'''
    # Prepare array of # occurrences of each modulus within the power list
    count = [0] * p
    for y in (pow(x, x, p) for x in xrange(1, m + 1)): count[y] += 1
    # Restrict array to non-zero entries
    a = filter(lambda x: x[1], enumerate(count))
    # Initial condition: first a-entry (k=0) + at most a single element used (n=1)
    w = [0L] * p
    w[0] += 1  # Empty set
    w[a[0][0]] += 1  # The set {r} where r is the first modulus in the a-list
    # DP over a-entries (k), within each DP on used k-th element count (n)
    for k, (r, c) in enumerate(a):
        for _ in xrange(2 if k == 0 else 1, c + 1):
            w = [(w[s] + w[(s - r) % p]) % t for s in xrange(p)]
    return w

if __name__ == "__main__":
    print num_subsets(250250L, 250L, 10 ** 16L)[0] - 1
