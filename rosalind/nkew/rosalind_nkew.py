'''
============================================================
http://rosalind.info/problems/nkew

In a weighted tree, each edge is assigned a (usually positive) number, called its weight. The distance between two nodes in a weighted tree becomes the sum of the weights along the unique path connecting the nodes.

To generalize Newick format to the case of a weighted tree T,
during our repeated "key step," if leaves v1,v2,...,vn are neighbors in T, and all these leaves are incident to u, then we replace u with (v1:d1,v2:d2,...,vn:dn)u, where di is now the weight on the edge {vi,u}.

Given: A collection of n weighted trees (n<=40) in Newick format, with each tree containing at most 200 nodes; each tree Tk is followed by a pair of nodes xk and yk in Tk.

Return: A collection of n numbers, for which the kth number represents the distance between xk and yk in Tk.
============================================================
'''
import StringIO
from Bio import Phylo

def read_cases(file_name):
    '''Read a tree and two branch names from file. Generator of those.'''
    with open(file_name, 'rb') as f:
        while True:
            try:
                s = f.next().strip()
                name1, name2 = f.next().strip().split()
                yield s, name1, name2
                f.next()  # Blank line in file - separates entries
            except StopIteration: break
            
def find_node_by_name(t, name):
    return t.find_elements(name=name).next()

def tree_distance(s, name1, name2):
    t = Phylo.read(StringIO.StringIO(s), 'newick')
    return int(t.distance(find_node_by_name(t, name1), find_node_by_name(t, name2)))
    
def nkew(f):
    '''Main driver to solve this problem.'''
    out = StringIO.StringIO()
    for s, name1, name2 in read_cases(f):
        out.write('%d ' % (tree_distance(s, name1, name2),))
    output_str = out.getvalue()[:-1]
    out.close()
    return output_str

if __name__ == "__main__":
    print nkew('rosalind_nkew_sample.dat')
    print nkew('rosalind_nkew.dat')
