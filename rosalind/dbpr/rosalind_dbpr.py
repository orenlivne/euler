'''
============================================================
http://rosalind.info/problems/dbpr

Given: The UniProt ID of a protein.

Return: A list of biological processes in which the protein is involved (biological processes are found in a subsection of the protein's "Gene Ontology" (GO) section).
============================================================
'''
import rosalind.rosutil as ro, rosdb as rd

def protein_biological_processes(protein):
    '''Return the list of biological processes a protein is involved in.'''
    record = rd.protein_record(protein)
    # Return all Gene Ontology (GO) records that start with "P:"
    return [x[2][2:] for x in record.cross_references if x[0] == 'GO' and x[2].startswith('P:')]

def dbpr(f):
    return '\n'.join(protein_biological_processes(ro.read_str(f)))

if __name__ == "__main__":
    # print dbpr('rosalind_dbpr_sample.dat')
    print dbpr('rosalind_dbpr.dat')
