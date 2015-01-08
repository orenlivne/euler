'''
============================================================
Common utilities relating to searching NCBI databases. 
============================================================
'''
from Bio import Entrez, SeqIO, ExPASy, SwissProt

Entrez.email = "god@heaven.gom"

def search(db, term):
    '''Return the e-search record of the squery ''term'' in the NCBI database ''db''.'''
    return Entrez.read(Entrez.esearch(db=db, term=term))

def num_records(db, term):
    '''Return the number of records of the squery ''term'' in the NCBI database ''db''.'''
    return int(search(db, term)['Count'])

#-----------------------
# GenBank - gene db
#-----------------------
def dna_seq_of_id(gid):
    '''Return the DNA string associated with the GenBank ID gid.'''
    handle = Entrez.efetch(db='nucleotide', id=gid, rettype='fasta')
    record = list(SeqIO.parse(handle, 'fasta'))[0]
    return record.seq.tostring()

#-----------------------
# UniProt - protein db
#-----------------------
def protein_record(protein):
    '''Return the SwissProt record of a protein with id protein.'''
    handle = ExPASy.get_sprot_raw(protein)  # you can give several IDs separated by commas
    return SwissProt.read(handle)  # use SwissProt.parse for multiple proteins
