'''
============================================================
http://rosalind.info/problems/long

For a collection of strings, a larger string containing every one of the smaller strings as a substring is called a superstring.

By the assumption of parsimony, a shortest possible superstring over a collection of reads serves as a candidate chromosome.

Given: At most 50 DNA strings whose length does not exceed 1 kbp in FASTA format (which represent reads deriving from the same strand of a single linear chromosome).

The dataset is guaranteed to satisfy the following condition: there exists a unique way to reconstruct the entire chromosome from these reads by gluing together pairs of reads that overlap by more than half their length.

Return: A shortest superstring containing all the given strings (thus corresponding to a reconstructed chromosome).
============================================================
'''
import rosalind.rosutil as ro, numpy as np, textwrap
from numpy.testing.utils import assert_equal

PREFIX, SUFFIX = range(2)

max_len = lambda S: max(len(x) for x in S)

def prefix_hashes(s, b, m):
    '''Return an array with a (rolling) hash of s[:j], j=0..len(s).'''
    h = 0L
    yield h
    for x in s:
        h = (b * h + ord(x)) % m
        yield h

def suffix_hashes(s, b, m):
    '''Return an array with a (rolling) hash of s[:j], j=0..len(s).'''
    h, bk = 0L, 1L
    yield h
    for x in reversed(s):
        h = (bk * ord(x) + h) % m
        yield h
        bk = (bk * b) % m

def fix_dictionary(S, fraction, hash_type='rolling', b=15485867L, m=32452843L):
    '''Build a list of dictionaries, one for each prefix/suffix ("fix") length. Each dictionary key is a
    fix, and the value is a list of S string indices i where fix is a prefix in s[i], and a list of
    i where fix is a suffix in S[i]. Only keys for which both lists are non-empty are included. Only fixes
    of length >= fraction*len(S[i]) in S[i] are considered.
    b, m = 15485867L, 32452843L # Must be large enough to prevent hash collisions'''
    d = [dict() for _ in xrange(max_len(S) + 1)]
    for i, s in enumerate(S):
        n = len(s)
        nf = int(n * fraction)
        if hash_type == 'rolling': hp, hs = list(prefix_hashes(s, b, m)), list(suffix_hashes(s, b, m))
        for j in xrange(n, nf - 1, -1):
            if hash_type == 'rolling':                       
                for k, h in ((PREFIX, hp[j]), (SUFFIX, hs[j])):
                    d[j].setdefault(h, [set(), set()])[k].add(i)
            else:
                for k, h in ((PREFIX, s[:j]), (SUFFIX, s[-j:])):
                    d[j].setdefault(h, [set(), set()])[k].add(i)
    return [dict((k, v) for k, v in x.iteritems() if len(v[PREFIX]) and len(v[SUFFIX])) for x in d]

def overlap_chain(d, m):
    '''Return a linked list: S-index of suffix -> S-index of prefix. That is, for each
    string in s, which string comes next in the patching process that follows.'''
    chain, incoming, num_zero_in_degree_nodes, l, done = {}, np.array([False] * m), m, len(d) - 1, False
    while not done:
        for p, s in d[l].itervalues():
            for i1 in s:
                for i2 in (i2 for i2 in p if i2 != i1):
                    if not incoming[i2]:
                        # print 'Adding edge', (i1, j1), '->', (i2, j2)
                        incoming[i2] = True
                        chain[i1] = (i2, l)
                        num_zero_in_degree_nodes -= 1
                        if num_zero_in_degree_nodes == 1:
                            done = True
                            break
                if done: break
            if done: break
        if done: break
        l -= 1
    return chain, np.where(~incoming)[0][0]
    
def patch_string(S, chain, head):
    t, i = '', head
    while True:
        si, (i, j) = S[i], chain[i]
        # print i, j, '->', i_next, i_next in chain, S[i], S[i][:-j]
        t += si[:-j]
        if not i in chain: break
    return t + S[i]

def assemble(S, fraction, hash_type='rolling'):
    return patch_string(S, *overlap_chain(fix_dictionary(S, fraction, hash_type=hash_type), len(S)))

def assemble_fafsa(file_name, fraction, hash_type='rolling'):
    return assemble(ro.fafsa_values(file_name), fraction, hash_type=hash_type)

#-----------------------------
# Testing
#-----------------------------
def print_fix_dictionary(d):
    fmt = '%%-%ds:' % (len(d) - 1,)
    for i, x in enumerate(d):
        print 'length', i
        for k, v in x.iteritems():
            print fmt % (k,), '%-30s\t%-30s' % (repr(list(v[PREFIX])), repr(list(v[SUFFIX])))

def test_assembly(S, t):
    assert_equal(assemble(S, 0.5), t, 'Wrong assembly result')

def test_hash_strategies_are_equivalent(file_name):
    a = assemble_fafsa(file_name, 0.5, hash_type='rolling')
    b = assemble_fafsa(file_name, 0.5, hash_type='prefix')
    assert_equal(a, b, 'Hash strategies did not result in the same assembled string')

if __name__ == "__main__":
    test_assembly(['ATTAGACCTG', 'CCTGCCGGAA', 'AGACCTGCCG', 'GCCGGAATAC'], 'ATTAGACCTGCCGGAATAC')
    test_hash_strategies_are_equivalent('rosalind_long_sample.dat')
    test_hash_strategies_are_equivalent('rosalind_long.dat')

    # Note: rolling hash was slower than using prefixes in this case, although it should have
    # a smaller complexity in general    
    print assemble_fafsa('rosalind_long_sample.dat', 0.5)
    print '\n'.join(textwrap.wrap(assemble_fafsa('rosalind_long.dat', 0.5)))
    