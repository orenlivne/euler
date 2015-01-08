'''
============================================================
http://rosalind.info/problems/dbru

Given: A collection of up to 1000 DNA strings of equal length (not exceeding 50 bp) corresponding to a set S of (k+1)-mers.

Return: The adjacency list corresponding to the de Bruijn graph corresponding to S U Src.
============================================================
'''
import rosalind.rosutil as ro

dbru = lambda f: '\n'.join('(%s, %s)' % (x[0], x[1]) for x in ro.de_bruijn_adj_list(ro.read_lines(f)))

if __name__ == "__main__":
#    print dbru('rosalind_dbru_sample.dat')   
    print dbru('rosalind_dbru.dat')
    
