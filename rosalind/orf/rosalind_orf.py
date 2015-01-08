'''
============================================================
http://rosalind.info/problems/orf

Problem

Either strand of a DNA double helix can serve as the coding strand for RNA transcription. Hence, a given DNA string implies six total reading frames, or ways in which the same region of DNA can be translated into amino acids: three reading frames result from reading the string itself, whereas three more result from reading its reverse complement.

An open reading frame (ORF) is one which starts from the start codon and ends by stop codon, without any other stop codons in between. Thus, a candidate protein string is derived by translating an open reading frame into amino acids until a stop codon is reached.

Given: A DNA string s of length at most 1 kbp in FASTA format.

Return: Every distinct candidate protein string that can be translated from ORFs of s. Strings can be returned in any order.
============================================================
'''
from rosalind.rosutil import DNA_TRANSLATION, DNA_START_CODON, DNA_STOP_CODONS, fafsa_itervalues, revc

def protein_strings(s):
    '''All possible protein sequences of the DNA string s. May yield duplicates.'''
    max_i = len(s) - 3
    for t in (s, revc(s)):
        for start in xrange(3):
            #print '---> t', t, 'start', start
            i, translate, starts, relative_index, p = start, False, [], 0, ''
            while i <= max_i:
                c = t[i:i + 3]
                #print 'i', i, 'c', c
                if c == DNA_START_CODON:
                    #i_start = i
                    starts.append(relative_index)
                    #print 'start', 'i', i, t[i:], 'starts', starts
                    translate = True
                if translate:
                    if c in DNA_STOP_CODONS:
                        #print 'stop ', 'i', i, t[i_start:i + 3]
                        #print 'p', p
                        for relative_index in starts:
                            #print 'yielding p[%d:] = %s' % (relative_index, p[relative_index:])  
                            yield p[relative_index:]
                        translate, relative_index, p = False, 0, ''
                        del starts[0:len(starts)]
                    else:
                        p = ''.join((p, DNA_TRANSLATION[c]))
                        #print 'translating', c, 'to', DNA_TRANSLATION[c], 'relative_index', relative_index
                        relative_index += 1
                i += 3

def distinct_protein_strings(s):
    return set(protein_strings(s))

if __name__ == "__main__":
#     for k, v in DNA_TRANSLATION.iteritems():
#         print k, ':', v
#     print DNA_START_CODON, DNA_STOP_CODONS
    #print '\n'.join(distinct_protein_strings(fafsa_itervalues('rosalind_orf_sample.dat').next()))
    print '\n'.join(distinct_protein_strings(fafsa_itervalues('rosalind_orf.dat').next()))
    