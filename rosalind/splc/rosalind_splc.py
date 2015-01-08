'''
============================================================
http://rosalind.info/problems/splc

After identifying the exons and introns of an RNA string, we only need to delete the introns and concatenate the exons to form a new string ready for translation.

Given: A DNA string s (of length at most 1 kbp) and a collection of substrings of s acting as introns. All strings are given in FASTA format.

Return: A protein string resulting from transcribing and translating the exons of s. (Note: Only one solution will exist for the dataset provided.)
============================================================
'''
import rosalind.rosutil as ro, itertools as it

def exons(s, introns):
    for intron in introns:
        i = s.find(intron)
        if i > 0: yield s[:i]
        s = s[i + len(intron):]
    if s: yield s

def dna_to_protein(s):
    '''Convert mRNA string to a protein string.'''
    return reduce(lambda x, y: ''.join((x, y)), it.takewhile(lambda v: v != ro.STOP_VALUE, (ro.DNA_TRANSLATION[s[i:i + 3]] for i in xrange(0, len(s), 3))), '')

def splice(s, introns):
    return ''.join(it.imap(dna_to_protein, exons(s, introns)))

def splc(f):
    s = list(ro.fafsa_itervalues(f))
    return splice(s[0], sorted(s[1:], key=lambda x: s[0].find(x)))
    
if __name__ == "__main__":
    print splc('rosalind_splc_sample.dat')
    print splc('rosalind_splc.dat')
