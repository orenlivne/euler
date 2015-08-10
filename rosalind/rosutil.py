'''
============================================================
Rosalind common utilities.
============================================================
'''
from __future__ import division
import os, itertools as it, re, numpy as np, networkx as nx
from collections import Counter
from scipy.special import betainc
from scipy.interpolate import interp1d
from scipy import stats

ROSALIND_HOME = os.path.dirname(os.path.realpath(__file__))

#---------------------------------------
# I/O
#---------------------------------------
'''Read string from a file.'''
read_str = lambda file_name: open(file_name, 'rb').readlines()[0].strip()

'''Read integer from a file.'''
read_int = lambda file_name: int(read_str(file_name))

'''Read all lines from a file.'''
iterlines = lambda file_name: (x.strip() for x in open(file_name, 'rb'))

'''Read all lines from a file.'''
read_lines = lambda file_name: [x.strip() for x in open(file_name, 'rb')]

'''Read a list of integers on a single space-separated line from a string.'''
to_int_list = lambda s: map(int, s.split())

'''Read a list of integers on a single space-separated line from a file.'''
read_ints_str = lambda file_name: map(int, read_str(file_name).split())

'''Read a set from a string in the format {1, 2, 3}.'''
read_int_set = lambda s: set(map(int, s.lstrip('{').rstrip('}').split(',')))

'''Read a single FAFSA string from a file.'''
read_fafsa = lambda file_name: fafsa_values(file_name)[0]

'''Skips the first n iterates of an iterate stream.'''
def skip(iterable, skip_amount):
    for _ in xrange(skip_amount): it = next(iterable)
    for x in iterable: yield x

'''Write a set into a string in the format {1, 2, 3}.'''
def repr_set(s):
    return '{' + ', '.join(map(str, s)) + '}'

'''Join a list into a string in the format 1 2 3.'''
def join_list(s, delimiter=' '):
    return delimiter.join(map(str, s))

def fafsa_itervalues(file_name):
    '''Read strings from file in FAFSA format. Generator.'''
    with open(file_name, 'rb') as f:
        for x in stream_fafsa_itervalues(f): yield x

def fafsa_values(file_name):
    '''Read strings from file in FAFSA format into a list.'''
    return list(fafsa_itervalues(file_name))

def fafsa_iteritems(file_name):
    '''Read FAFSA format entries from the file name file_name. Return a list of (label, data) tuples. Generator.'''
    with open(file_name, 'rb') as f:
        for x in stream_fafsa_iteritems(f): yield x

def fafsa_items(file_name):
    '''Read FAFSA format entries from the file name file_name. Return a list of (label, data) tuples. Returns a list.'''
    return list(fafsa_iteritems(file_name))

def stream_fafsa_itervalues(f):
    '''Read strings from stream in FAFSA format.'''
    buf = ''
    for line in (line.strip() for line in f):
        if line.startswith('>'):
            # Reached a new header, output previous string if exists in the buffer
            if buf:
                yield buf
                buf = ''  # Clear buffer
        else: buf += line  # Concatenate string lines in the buffer
    # Emit last string
    if buf: yield buf

def stream_fafsa_iteritems(f):
    '''Read FAFSA format entries from the stream f. Return a list of (label, data) tuples.'''
    label, buf = '', ''
    for line in (line.strip() for line in f):
        if line.startswith('>'):
            # Record new label
            new_label = line[1:]
            if not label: label = new_label
            # Reached a new header, output previous entry if exists in the buffer
            if buf:
                yield label, buf
                buf = ''  # Clear buffer for next entry
                label = new_label  # This is the label of the next entry, already read it above
        else: buf += line  # Concatenate string lines in the buffer
    # Emit last entry
    if buf: yield label, buf

#---------------------------------------
# Mass Spectrometry
#---------------------------------------
'''Amino-acid-letter-to-mass converter.'''
aa_mass = dict((x[0], float(x[1])) for x in (x.split() for x in open(ROSALIND_HOME + '/dat/aa-mass.dat', 'rb')))

def _aa_of_mass():
    '''Return the amino acid letter of mass m.'''
    aa, mass = zip(*sorted(aa_mass.iteritems(), key=lambda x: x[1]))
    f = interp1d(mass, xrange(len(aa)), 'nearest')
    def g(m):
        if m < mass[0]: return aa[0]
        elif m > mass[-1]: return aa[-1]
        else: return aa[int(f(m))]
    return g

'''Mass-to-nearest-amino-acid-letter converter.'''
aa_of_mass = _aa_of_mass()

def aa_of_mass_exact(x, tol=1e-2):
    '''Return amino acid letter of the mass x if x is within tol-tolerance from the nearest
    amino-acid mass.'''
    mass = aa_of_mass(x)
    y = aa_mass[mass]
    return mass if np.abs(x - y) <= tol else None
    
# Not completely useful yet...
#
# class MassDict(Counter):
#     '''An amino acid mass dictionary. Lumps floating-point keys that are close to the same bin.'''  
# 
#     def __init__(self, tol, items):
#         self.tol = tol
#         for x in items: self.
#     
#     @staticmethod
#     def add_with_tol(self, x):
#         '''Add x to closest .'''
#         a = mdict()
#         for k, v in items: a[k] = v
#         return a
    
#---------------------------------------
# Mathematical & Statistical functions
#---------------------------------------
iabs = lambda x: x if x >= 0 else -x

def log_factorial(N):
    '''Return an array of log(n) values for n = 0..N.'''
    L = [0] * (N + 1)
    for n in xrange(2, N + 1): L[n] = L[n - 1] + np.log(n)
    return L

def log10_factorial(N):
    '''Return an array of log10(n) values for n = 0..N.'''
    L = [0] * (N + 1)
    for n in xrange(2, N + 1): L[n] = L[n - 1] + np.log10(n)
    return L

def binom():
    '''A generator of binomial coefficients. Iterate n returns [C(n,k) for k in xrange(n)], n = 0,1,2,... .'''
    b = [1L]
    yield list(b)
    for n in it.count(1):
        a = list(b)
        for i in xrange(n - 1): b[i] = a[i] + a[i + 1]
        b.insert(0, 1L)
        yield list(b)

def binom_mod(r):
    '''A generator of binomial coefficients modulo r >= 2.
    Iterate n returns [C(n,k) for k in xrange(n)], n = 0,1,2,... .'''
    b = [1L]
    yield list(b)
    for n in it.count(1):
        a = list(b)
        for i in xrange(n - 1): b[i] = (a[i] + a[i + 1]) % r
        b.insert(0, 1L)
        yield list(b)

def sum_mod(iterable, r):
    '''Summation modulo r of the iterates of iterable.'''
    return reduce(lambda x, y: (x + y) % r, iterable, 0)

def prod_mod(iterable, r):
    '''Product modulo r of the iterates of iterable.'''
    return reduce(lambda x, y: (x * y) % r, iterable)

def bernoulli(n, p, k):
    '''Probability of getting k successes in n Bernoulli trials with success probability p.'''
    if k < 0 or k > n: return 0
    if p == 0: return 1 if k == 0 else 0
    if p == 1: return 1 if k == n else 0
    return stats.binom(n, p).pmf(k)

def cumbin(n, p, m):
    '''Cumulative binomial disribution - probability of getting <= m successes in n Bernoulli trials
    with success probability p.'''
    return betainc(n - m, m + 1, 1 - p)

#---------------------------------------
# Population Dynamics
#---------------------------------------
def wf_pmf(n, m):
    '''WF model, distribution of major allele, population of n alleles, with initially m major alleles.
    Geneator of distributions of successive generations.'''
    b = [[bernoulli(n, i / n, k) for k in xrange(n + 1)] for i in xrange(n + 1)]
    x = [0] * (n + 1); x[m] = 1
    while True:
        x = [sum(b[i][k] * x[i] for i in xrange(n + 1)) for k in xrange(n + 1)]
        yield x

#---------------------------------------
# DNA symbol functions
#---------------------------------------
ALPHABET = 'ACGT'
gc_count = lambda s: sum(1 for x in s if x in 'GC')
gc_content = lambda s: float(gc_count(s)) / len(s)
'''Generalized GC content - k-mer composition of a string s.'''
kmer_composition = lambda s, k, alphabet = ALPHABET: [(v - 1) for _, v in sorted((Counter(''.join(x) for x in it.product(alphabet, repeat=k)) + Counter(s[i:i + k] for i in xrange(len(s) - k + 1))).iteritems())]

'''Reverse complement coding of DNA letters.'''
COMPLEMENT = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
revc = lambda s: ''.join(map(COMPLEMENT.get, reversed(s)))

'''Mapping of codon to proteins. Load from text file.'''
_ROSALIND_DIR = os.path.dirname(os.path.realpath(__file__))
_CODON_TABLE_FILE_NAME = _ROSALIND_DIR + '/dat/codon-table.dat'
RNA_TRANSLATION = dict(x.split(' ') for x in read_lines(_CODON_TABLE_FILE_NAME))
RNA_START_CODON = 'AUG'  # The special key of the start codons in CODON dictionary
STOP_VALUE = 'Stop'  # The special value of stop codons in CODON dictionary
'''Reverse complement coding of RNA letters.'''
RNA_COMPLEMENT = {'A':'U', 'U':'A', 'C':'G', 'G':'C'}

DNA_TRANSLATION = dict((k.replace('U', 'T'), v) for k, v in (x.split() for x in read_lines(_CODON_TABLE_FILE_NAME)))
DNA_START_CODON = RNA_START_CODON.replace('U', 'T')
DNA_STOP_CODONS = set(k for k, v in DNA_TRANSLATION.iteritems() if v == STOP_VALUE)

#---------------------------------------
# Modulo arithmetic
#---------------------------------------
def extended_gcd(a, b):
    '''Returns the coefficients x,y of a*x + b*y = gcd(a,b). Extended Euclid''s algorithm.'''
    x, y, lastx, lasty = 0L, 1L, 1L, 0L
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        x, y, lastx, lasty = lastx - q * x, lasty - q * y, x, y
    return lastx, lasty

'''Return the unique multiplicative inverse of x mod p, if exists.'''
inv_mod = lambda x, p: extended_gcd(x, p)[0]

#---------------------------------------
# Pattern matching
#---------------------------------------
def substrings(s):
    return [s[i:j] for i in xrange(len(s)) for j in xrange(i + 1, len(s) + 1)]

def hamm(s, t):
    '''Return the Hamming distance between two s and t of the same length.''' 
    return sum(x != y for (x, y) in zip(s, t))

def find_all(text, pattern):
    '''Return all pattern start indices in text.'''
    return (m.start() for m in re.finditer('(?=%s)' % (pattern,), text))

def kmers(s, k):
    '''A generator of all k-mers in the string s.''' 
    return (s[i:i + k] for i in xrange(len(s) - k + 1))

def kmer_counter(s, k):
    '''k-mer Counter object (counts of all k-mer occurrences in the string s).''' 
    return Counter(kmers(s, k))

def most_frequent(c):
    '''Return the list of most-frequent k-mers in the Counter c.'''
    count_max = c.most_common(1)[0][1]
    return (value for value, count in c.iteritems() if count == count_max)

def most_frequent_kmers(s, k):
    '''Return the list of most-frequent k-mers in s (a generator).'''
    return most_frequent(Counter(kmers(s, k)))

def substitute(s, motif, location):
    '''Substitute the substring of s comprising of locations location with
    the corresponding letters of motif.'''
    l = list(s)
    for i in xrange(len(motif)): l[location[i]] = motif[i]
    return ''.join(l)
 
def possible_kmers(x, d):
    '''Return all possible k-mers that are Hamming-distance-d from x.'''
    return set(substitute(x, motif, location) for r in xrange(d + 1)
               for location in it.combinations(xrange(len(x)), r)
               for motif in it.product(ALPHABET, repeat=r))

def possible_kmers_counter(s, k, d):
    '''Return the counts of all possible k-mers that are Hamming-distance-d away
    from a k-mer of s.'''
    return Counter(y for x in kmers(s, k) for y in possible_kmers(x, d))
        
def most_frequent_approx(s, k, d):
    '''Return the most frequent k-mers up to d mismatches in s.'''
    return most_frequent(possible_kmers_counter(s, k, d))

def flatten_counter(c):
    '''Flatten a Counter to a list.'''
    l = []
    for k, v in c.iteritems():
        for _ in xrange(v): l.append(k)
    return l

#---------------------------------------
# Genome assembly
#---------------------------------------
'''de-Bruijn graph adjacency list of a set of kmers r.'''
de_bruijn_adj_list = lambda S: set((r[:-1], r[1:]) for r in it.chain(S, it.imap(revc, S)))
'''de-Bruijn graph of a set of k-mers r.'''
de_bruijn_graph = lambda r: nx.from_edgelist(de_bruijn_adj_list(r), create_using=nx.DiGraph())

#---------------------------------------
# Linear algebra
#---------------------------------------
'''Create an m x n 2-D integer array filled with zeros.'''
zeros_int_array = lambda m, n: [[0 for _ in xrange(n)] for _ in xrange(m)]

'''Create an m x n 2-D boolean array filled with False values.'''
zeros_bool_array = lambda m, n: [[False for _ in xrange(n)] for _ in xrange(m)]

#---------------------------------------
# Testing, random data generation
#---------------------------------------
def random_string(n, alphabet=ALPHABET):
    '''Return a uniformly random string of length n using the alphabet alphabet.''' 
    return ''.join(alphabet[i] for i in np.random.randint(0, len(alphabet) - 1, n))

#---------------------------------------
# Dynamic programming
#---------------------------------------
def memoize(f):
    '''Decorate a function f with a memo (cache).'''
    cache = {}
    def decorated_function(*args):
        if args not in cache: cache[args] = f(*args)
        return cache[args]
    return decorated_function
