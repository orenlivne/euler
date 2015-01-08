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
def commonOverlapIndexOf(text1, text2):
    '''Calculate the overlap of text1, text2 using find().
    Taken from https://neil.fraser.name/news/2010/11/04/'''
    # Cache the text lengths to prevent multiple calls.
    text1_length = len(text1)
    text2_length = len(text2)
    # Eliminate the null case.
    if text1_length == 0 or text2_length == 0: return 0
    # Truncate the longer string.
    if text1_length > text2_length: text1 = text1[-text2_length:]
    elif text1_length < text2_length: text2 = text2[:text1_length]
    # Quick check for the worst case.
    if text1 == text2: return min(text1_length, text2_length)
 
    # Start by looking for a single character match
    # and increase length until no match is found.
    best = 0
    length = 1
    while True:
        pattern = text1[-length:]
        found = text2.find(pattern)
        print length, pattern, found
        if found == -1: return best
        length += found
        if text1[-length:] == text2[:length]:
            best = length
            length += 1
            print 'best', best

PREFIX, SUFFIX = range(2)

def fix_dictionary(S, fraction):
    N = max(len(x) for x in S)
    
    # TODO:
    
    d = [dict() for _ in xrange(N + 1)]
    for i, s in enumerate(S):
        m = len(s)
        mf = int(m * fraction)
        for j in xrange(m, mf - 1, -1):
            h = s[:j]
            d[len(h)].setdefault(h, [set(), set()])[PREFIX].add((i, j))
            h = s[-j:]
            d[len(h)].setdefault(h, [set(), set()])[SUFFIX].add((i, j))
    
    # Remove entries where no strings non-overlap (they only appear in a single string as a prefix or suffix)
    return [dict((k, v) for k, v in x.iteritems() if len(v[PREFIX]) >= 1 and len(v[SUFFIX]) >= 1) for x in d]

def print_fix_dictionary(d):
    fmt = '%%-%ds:' % (len(d) - 1,)
    for i, x in enumerate(d):
        print 'length', i
        for k, v in x.iteritems():
            print fmt % (k,), '%-30s\t%-30s' % (repr(list(v[PREFIX])), repr(list(v[SUFFIX])))

if __name__ == "__main__":
    # print commonOverlapIndexOf('CCTGCCGGAA', 'CGGAATCCTGC')
    
    # S = ['ATTAGACCTG', 'CCTGCCGGAA', 'AGACCTGCCG', 'GCCGGAATAC']
    # S = ['ATTAGACCTG', 'TTAGACCTGT', 'TAGACCTGTC', 'AGACCTGTCG']
    #S = ['AAAAAAAAAA', 'AAAAAAAAAB', 'AAAAAAAABA', 'AAAAAAABAA']
    S = ['AAAAAA', 'AAAAABA', 'AAAAAB', 'AAAABA', 'AAABAA']
    d = fix_dictionary(S, 0.5)
    print_fix_dictionary(d)
