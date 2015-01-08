'''
============================================================
http://rosalind.info/problems/mprt

Motif Implies Functionclick to expand

Problem

To allow for the presence of its varying forms, a protein motif is represented by a shorthand as follows: [XY] means "either X or Y" and {X} means "any amino acid except X." For example, the N-glycosylation motif is written as N{P}[ST]{P}.

You can see the complete description and features of a particular protein by its access ID "uniprot_id" in the UniProt database, by inserting the ID number into

http://www.uniprot.org/uniprot/uniprot_id
Alternatively, you can obtain a protein sequence in FASTA format by following

http://www.uniprot.org/uniprot/uniprot_id.fasta
For example, the data for protein B5ZC00 can be found at http://www.uniprot.org/uniprot/B5ZC00.

Given: At most 15 UniProt Protein Database access IDs.

Return: For each protein possessing the N-glycosylation motif, output its given access ID followed by a list of locations in the protein string where the motif can be found.
============================================================
'''
import re, urllib2, rosutil as ro, numpy as np

'''Load a protein string from the UnitProt online database.'''
protein_of_id = lambda protein_id: ro.stream_fafsa_itervalues(urllib2.urlopen('http://www.uniprot.org/uniprot/%s.fasta' % (protein_id,))).next()

def motif_matches(iterable, motif):
    regex = re.compile(motif)
    for s in iterable:
        matches = []
        protein = protein_of_id(s)
        while True:
            match = regex.search(protein)
            if not match: break
            matches.append(match)
            protein = protein[match.start() + 1:]  # Back up two to get the UG portion.  Shouldn't matter, but safer.
        yield s, np.cumsum([m.start() + 1 for m in matches], dtype=int)
        
def print_matches(matches):
    for s, m in matches:
        if len(m): print s + '\n' + ' '.join(map(str, m))

if __name__ == "__main__":
    print_matches(motif_matches(ro.read_lines('rosalind_mprt.dat'), 'N[^P][ST][^P]'))
