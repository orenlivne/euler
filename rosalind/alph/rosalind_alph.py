'''
============================================================
http://rosalind.info/problems/alph

Given: A rooted binary tree T on n (n<=500) species, given
in Newick format, followed by a multiple alignment of m
(m<=n) augmented DNA strings having the same length (at most
300 bp) corresponding to the species and given in FASTA
format.

Return: The minimum possible value of dH(T), followed by a
collection of DNA strings to be assigned to the internal
nodes of T that will minimize dH(T) (multiple solutions will
exist, but you need only output one).
============================================================
'''
import rostree as rt
from Bio.SeqIO.FastaIO import FastaIterator 

def build_options(t, d, gap_symbol='-'):
    '''Given a tree t and leaf DNA data d at one locus, build the ancestral options = set at each
    non-leaf node of t. Return a t.node_index-indexed array of those sets.'''
    stack, s = [], [None] * t.num_nodes
    for node in t.find_clades(order='postorder'):
        i = t.node_index[node.name]
        if node.is_terminal():
            x = d[i]
            options = set(x)
        else:
            o1, o2 = stack.pop(), stack.pop()
            common = o1 & o2
            options = common if common else (o1 | o2)
        stack.append(options)
        s[i] = options
    return s
    
def dist(x, y):
    '''Character distance between x and y. Substitution, indels all count as 1.'''
    return 0 if x == y else 1
                 
def select_options(t, s, d):
    '''Walk the tree t top-down, and select an option from each option set s at each non-leaf
    node to minimize the total Hamming distance on the tree. Return an array of select ancestral
    letters and the corresponding minimum total Hamming distance.'''
    # Assign the root
    i = t.node_index[t.root.name]
    d[i], D = next(iter(s[i])), 0
    for node in (x for x in t.find_clades(order='preorder') if x.parent):
        i, dp = t.node_index[node.name], d[t.node_index[node.parent.name]]
        if not node.is_terminal():
            o = s[i]
            # Let u_c be the selected letter at node u and S_u the option set it's selected from.
            # For each internal node v, if v's parent u satisfies $u_c \in S_v$, set
            # $v_c \leftarrow u_c$; Otherwise, (including for the root node), arbitrarily
            # assign  any $t \in S_v$ to vc.
            d[i] = dp if dp in o else next(iter(o))
        D += dist(dp, d[i])
    return d, D

def aug_tree(t):
    '''Augment the tree t with node index and number of nodes fields.'''
    t.node_index = dict((x.name, i) for i, x in enumerate(t.find_clades(order='postorder')))  # Any other order would be good too as long as we consistently use this array to refer to tree nodes 
    t.num_nodes = len(t.node_index)

def array_append(a, b):
    '''a += b elementwise for a,b = string arrays of equal lengths.'''
    for i in xrange(len(a)): a[i] += b[i]
    
def extract_character(t, d_leaf, j):
    '''Extract character #j at all nodes from the sequence array d.'''
    dj = ['' for _ in xrange(t.num_nodes)]
    for i in (t.node_index[x.name] for x in t.get_terminals()): dj[i] = d_leaf[i][j]
    return dj

def infer(t, d_leaf, gap_symbol='-'):
    '''Infer non-leaf nodes. Return d_H(T) and a corresponding assignment of nodes to DNA strings.
    Internal nodes may contain the gap symbol.''' 
    n = t.num_nodes
    d, D = ['' for _ in xrange(n)], 0
    # Do each DNA character separately; append them to the d array and D counter
    for j in xrange(len(d_leaf[0])):
        dj = extract_character(t, d_leaf, j)
        s = build_options(t, dj, gap_symbol=gap_symbol)
        dj, Dj = select_options(t, s, dj)
        array_append(d, dj)
        D += Dj
    return dict((x.name, d[t.node_index[x.name]]) for x in t.find_clades() if not x.is_terminal()), D

def load_file(file_name):
    '''Load tree, leaf DNA strings from file.'''
    f = open(file_name, 'rb')
    t = rt.read_newick_str(f.readline().strip())
    aug_tree(t)
    d_leaf = ['' for _ in xrange(t.num_nodes)]
    for record in FastaIterator(f): d_leaf[t.node_index[record.id]] = record.seq
    return t, d_leaf

def alph(file_name):
    '''Main driver to solve this problem.'''
    t, d_leaf = load_file(file_name)
    d_internal, D = infer(t, d_leaf)
    print D
    for k, v in d_internal.iteritems():
        print '>' + k
        print v

if __name__ == "__main__":
#    alph('rosalind_alph_sample.dat')
    alph('rosalind_alph.dat')
