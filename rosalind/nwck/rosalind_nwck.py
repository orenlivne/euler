'''
============================================================
http://rosalind.info/problems/nwck

Newick format is a way of representing trees even more concisely than using an adjacency list, especially when dealing with trees whose internal nodes have not been labeled.

First, consider the case of a rooted tree T. A collection of
leaves v1,v2,...,vn of T are neighbors if they are all adjacent
to some internal node u. Newick format for T is obtained by
iterating the following key step: delete all the edges {vi,u} from T and label u with (v1,v2,...,vn)u. This process is repeated all the way to the root, at which point a semicolon signals the end of the tree.

A number of variations of Newick format exist. First, if a node is not labeled in T, then we simply leave blank the space occupied by the node. In the key step, we can write (v1,v2,...,vn) in place of (v1,v2,...,vn)u if the vi are labeled; if none of the nodes are labeled, we can write (,,...,).

A second variation of Newick format occurs when T is unrooted, in which case we simply select any internal node to serve as the root of T. A particularly peculiar case of Newick format arises when we choose a leaf to serve as the root.

Note that there will be a large number of different ways to represent T in Newick format; see Figure 1.

Given: A collection of n trees (n<=40) in Newick format, with each tree containing at most 200 nodes; each tree Tk is followed by a pair of nodes xk and yk in Tk.

Return: A collection of n positive integers, for which the kth integer represents the distance between xk and yk in Tk.
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
    
def nwck(f):
    '''Main driver to solve this problem.'''
    out = StringIO.StringIO()
    for s, name1, name2 in read_cases(f):
        out.write('%d ' % (tree_distance(s, name1, name2),))
    output_str = out.getvalue()[:-1]
    out.close()
    return output_str

if __name__ == "__main__":
    print nwck('rosalind_nwck_sample.dat')
    print nwck('rosalind_nwck.dat')
