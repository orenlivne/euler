'''
============================================================
http://rosalind.info/problems/grph

A Brief Introduction to Graph Theoryclick to expand

Problem

A graph whose nodes have all been labeled can be represented by an adjacency list, in which each row of the list contains the two node labels corresponding to a unique edge.

A directed graph (or digraph) is a graph containing directed edges, each of which has an orientation. That is, a directed edge is represented by an arrow instead of a line segment; the starting and ending nodes of an edge form its tail and head, respectively. The directed edge with tail v and head w is represented by (v,w) (but not by (w,v)). A directed loop is a directed edge of the form (v,v).

For a collection of strings and a positive integer k, the overlap graph for the strings is a directed graph Ok in which each string is represented by a node, and string s is connected to string t with a directed edge when there is a length k suffix of s that matches a length k prefix of t, as long as s != t; we demand s != t to prevent directed loops in the overlap graph (although directed cycles may be present).

Given: A collection of DNA strings in FASTA format having total length at most 10 kbp.

Return: The adjacency list corresponding to O3. You may return edges in any order.
============================================================
'''
from rosalind.rosutil import fafsa_iteritems

def overlap_graph_adjlist(entries, k):
    '''Generator of the overlap graph O_k adjacency list element from a list of FAFSA-formatted
    file (label, string) entries. Runtime: O(|V|+|E|). Storage: O(|V|).'''
    # Index labels by prefixes and suffixes
    prefix, suffix = {}, {}
    for label, s in entries:
        a = s[:k]; prefix.setdefault(a, []).append(label)
        a = s[-k:]; suffix.setdefault(a, []).append(label)
    # For each dictionary key (=fix), connect labels of suffixes to labels of prefixes
    for a, S in suffix.iteritems():
        if a in prefix:
            T = prefix[a]
            for s in S:
                for t in T:
                    if s != t: yield s, t
    
def write_adjlist(adjlist):
    for s, t in adjlist: print s, t

def overlap_graph_fafsa(file_name):
    write_adjlist(overlap_graph_adjlist(fafsa_iteritems(file_name), 3))
    
if __name__ == "__main__":
    #overlap_graph_fafsa('rosalind_grph_sample.dat')
    overlap_graph_fafsa('rosalind_grph.dat')
    
