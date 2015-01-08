'''
============================================================
http://rosalind.info/problems/corr

As is the case with point mutations, the most common type of sequencing error occurs when a single nucleotide from a read is interpreted incorrectly.

Given: A collection of up to 1000 reads of equal length (at most 50 bp) in FASTA format. Some of these reads were generated with a single-nucleotide error. For each read s in the dataset, one of the following applies:

s was correctly sequenced and appears in the dataset at least twice (possibly as a reverse complement);
s is incorrect, it appears in the dataset exactly once, and its Hamming distance is 1 with respect to exactly one correct read in the dataset (or its reverse complement).
Return: A list of all corrections in the form "[old read]->[new read]". (Each correction must be a single symbol substitution, and you may return the corrections in any order.)
============================================================
'''

'''All solutions I glanced over on the rosalind website seem to be brute force, which has a complexity of
$O(m n^2)$ where m=size of strings and n=number of strings if the number of erroneous strings is comparable
with the number of correct strings. I enclose a divide-and-conquer algorithm that, except for extreme
data-dependent conditions, should run in $O(m n)$. For an easier binary-tree build-up, m is first
rounded up to the next power of two.'''
import rosalind.rosutil as ro, numpy as np

def char_dict(s):
    '''Divide step. Return a list of dictionaries, one for each position of an s-string,
    listing the indices of strings that include a character at that position.'''
    m, n = len(s[0]), len(s)
    d = [{} for _ in xrange(m)]
    for j in xrange(m):
        dj = d[j]
        for i in xrange(n): dj.setdefault(s[i][j], []).append(i)
    return d

def merge_candidates(L, R):
    '''Conquer step.'''
    return (L[0] & R[0], ((L[0] & R[1]) | (L[1] & R[0])) - (L[1] & R[1]))

def match_index_of(d, a):
    '''Divide-and-conquer for returning the index in the standardized string list of an error
    string a''s match.'''
    # Initialize - finest level
    C = [(set(dj[x]), reduce(set.union, (set(dj[y]) for y in dj if y != x), set())) for x, dj in zip(a, d)]
    # Aggregate till coarsest level
    while len(C) > 1: C = [merge_candidates(C[2 * j], C[2 * j + 1]) for j in xrange(len(C) / 2)]
    return iter(C[0][1]).next()

def next_two_power(m):
    '''Return the smallest 2-power >= m.'''
    x = 1
    while x < m: x *= 2
    return x

def pad_to_next_two_power(s):
    m = len(s[0])
    k = next_two_power(m)
    return (s if k == m else [x.ljust(k, 'A') for x in s], k - m)

def classify(s):
    '''Return the list of correct strings (standardized to start with ''A'' or ''T'')
    and incorrect strings in the collection s.'''
    d, correct = {}, np.tile(False, len(s))
    for i, x in enumerate(s):
        y = min(x, ro.revc(x))  # y = standardized form of x
        d.setdefault(y, []).append(i)
    # Find correct strings that occur exactly twice
    correct[np.array([x for (y, X) in d.iteritems() for x in X if len(X) >= 2])] = True
    return [y for (y, X) in d.iteritems() if len(X) >= 2], [s[x] for x in np.where(~correct)[0]]

def match_errors(s):
    '''A generator of error string -> correct string match.'''
    m, (y, e) = len(s[0]), classify(s)
    y = y + map(ro.revc, y)
    y, pad = pad_to_next_two_power(y)
    k = m + pad
    d = char_dict(y)
    for a in e: yield a, y[match_index_of(d, a.ljust(k, 'A'))][:-pad]
    
def corr(f):
    '''Finds and prints all matches, probably with an average complexity of O(n m log m) where n=#strings
    and m = size of strings.''' 
    return '\n'.join('%s->%s' % x for x in match_errors(ro.fafsa_values(f)))

if __name__ == "__main__":
    print corr('rosalind_corr.dat')
