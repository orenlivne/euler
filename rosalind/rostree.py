'''
============================================================
A binary ordered tree example from
http://code.activestate.com/recipes/286239-binary-ordered-tree/

Created on Dec 24, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import StringIO, numpy as np, rosalind.rosutil as ro
from Bio import Phylo

#------------------------
# Phylo package trees
#------------------------
def aug_tree(t):
    '''Augment a Phylo tree nodes with children and postorder number.'''
    t.root.parent = None
    t.root.prev_child = None

    for i, node in enumerate(t.find_clades(order='postorder')):
        node.postorder = i
        if not node.is_terminal():
            children = list(node)
            for i, child in enumerate(children):
                child.parent = node
                child.prev_child = None if i == 0 else children[i - 1]
                
    for node in (x for x in t.find_clades(order='preorder') if x.parent and not x.prev_child): node.prev_child = node.parent.prev_child
    return t

def read_newick(f, augment=True):
    '''Read a tree from file in Newick format and augment it with our useful traversal information.'''
    t = Phylo.read(f, 'newick')
    if augment: t = aug_tree(t)
    return t

def read_newick_str(s, augment=True):
    '''Read a tree from string in Newick format and augment it with our useful traversal information.'''
    return read_newick(StringIO.StringIO(s))

#------------------------
# Our binary tree impl
#------------------------
def split_branches(s):
    depth = 0
    for i, x in enumerate(s):
        if x == ',' and depth == 1: return s[1:i], s[i + 1:-1] 
        if x == '(': depth += 1
        elif x == ')': depth -= 1
    
def parse_newick(s):
    return _parse_newick(s[:-1])  # Trim the trailing ';'

def _parse_newick(s):
    t = BinaryTree()
    if s.startswith('('):  # Node
        parts = split_branches(s)
        t.left = _parse_newick(parts[0])
        t.right = _parse_newick(parts[1])
    else: t.data = s  # Leaf
    return t

####################################################################################
class BinaryTree(object):
    '''A simple binary tree.'''
    def __init__(self): self.left, self.right, self.data = None, None, None
    def __repr__(self): return self.__repr()
    def __repr(self, level=0):
        ret = '\t' * level + repr(self.data) + '\n'
        for child in (self.left, self.right): ret += child.__repr(level + 1) if child else ('\t' * (level + 1) + '-\n')
        return ret
    
#------------------------
# Binary Search Tree
#------------------------
class CNode:
    '''A node in a binary search tree.'''
    left, right, data = None, None, 0
    
    def __init__(self, data):
        # initializes the data members
        self.left = None
        self.right = None
        self.data = data

class CBOrdBinaryTree:
    '''Binary search tree.'''
    def __init__(self):
        # initializes the root member
        self.root = None
    
    def addNode(self, data):
        # creates a new node and returns it
        return CNode(data)

    def insert(self, root, data):
        # inserts a new data
        if root == None:
            # it there isn't any data
            # adds it and returns
            return self.addNode(data)
        else:
            # enters into the tree
            if data <= root.data:
                # if the data is less than the stored one
                # goes into the left-sub-tree
                root.left = self.insert(root.left, data)
            else:
                # processes the right-sub-tree
                root.right = self.insert(root.right, data)
            return root
        
    def lookup(self, root, target):
        # looks for a value into the tree
        if root == None:
            return 0
        else:
            # if it has found it...
            if target == root.data:
                return 1
            else:
                if target < root.data:
                    # left side
                    return self.lookup(root.left, target)
                else:
                    # right side
                    return self.lookup(root.right, target)
        
    def minValue(self, root):
        # goes down into the left
        # arm and returns the last value
        while(root.left != None):
            root = root.left
        return root.data

    def maxDepth(self, root):
        if root == None:
            return 0
        else:
            # computes the two depths
            ldepth = self.maxDepth(root.left)
            rdepth = self.maxDepth(root.right)
            # returns the appropriate depth
            return max(ldepth, rdepth) + 1
            
    def size(self, root):
        if root == None:
            return 0
        else:
            return self.size(root.left) + 1 + self.size(root.right)

    def printBinaryTree(self, root):
        # prints the tree path
        if root == None:
            pass
        else:
            self.printBinaryTree(root.left)
            print root.data,
            self.printBinaryTree(root.right)

    def printRevBinaryTree(self, root):
        # prints the tree path in reverse
        # order
        if root == None:
            pass
        else:
            self.printRevBinaryTree(root.right)
            print root.data,
            self.printRevBinaryTree(root.left)

#------------------------
# BinaryTree tests
#------------------------

def test_binary_search_tree():
# create the binary tree
    BBinaryTree = CBOrdBinaryTree()
    # add the root node
    root = BBinaryTree.addNode(0)
    # ask the user to insert values
    for i in range(0, 5):
        data = int(raw_input('insert the node value nr %d: ' % i))
        # insert values
        BBinaryTree.insert(root, data)
    print
    
    BBinaryTree.printBinaryTree(root)
    print
    BBinaryTree.printRevBinaryTree(root)
    print
    data = int(raw_input('insert a value to find: '))
    if BBinaryTree.lookup(root, data): print 'found'
    else: print 'not found'
        
    print BBinaryTree.minValue(root)
    print BBinaryTree.maxDepth(root)
    print BBinaryTree.size(root)
    
def test_binary_tree():
    root = BinaryTree()
    root.data = 'root'
    root.left = BinaryTree()
    root.left.data = 'left'
    root.right = BinaryTree()
    root.right.data = 'right'
    print root
    
'''Load character set in binary string matrix format from the file f.'''
load_character_set = lambda f: np.array([map(int, line) for line in ro.iterlines(f)])

def char_table_binary_string(c):
    '''Convert character set to a binary string.'''
    f = StringIO.StringIO()
    np.savetxt(f, c, fmt='%d', delimiter='')
    return f.getvalue()

def char_table(t, mapping=None):
    '''Encode a Phylo tree\'s splits as a binary matrix (character set table)). mapping is a dictionary
    that maps leaf node names into serial numbers 0..n-1, n=#leaves. If none, assuming leaf i is named
    \'ai\'.'''
    mapping = mapping.__getitem__ if mapping else lambda x: int(x.name[1:])
    non_term = list(t.get_nonterminals())
    n = len(non_term) + 2
    c, i = np.zeros((n - 3, n), dtype=int), 0
    ci = np.zeros((n,), dtype=int)
    #print 'char_table(n=%d)' % (n,)
    for x in non_term:
        #print i
        ci[:] = 0
        ci[np.array([mapping(x.name) for x in x.get_terminals()])] = 1
        if len(np.where(ci == 0)[0]) > 0: c[i], i = ci, i + 1
    return standardize_char_table(c)

def standardize_char_table(c):
    '''Standardize a split character set table so that all rows start with 0.
    Lexicographically sort rows.'''
    c = c.copy()
    #print 'standardize_char_table()'
    for i in xrange(c.shape[0]):
        #print i
        if c[i, 0] != 0: c[i] = 1 - c[i]
    return c[np.lexsort(c.transpose())]

'''Convert a character set table to a set of binary strings, each representing a split.'''
char_table_to_set = lambda c: set(ro.join_list(x, delimiter='') for x in c)

'''Convert a tree\'s character set table to a set of binary strings, each representing a split.'''
tree_to_set = lambda t, s: char_table_to_set(char_table(t, mapping=dict((x, i) for i, x in enumerate(s))))

'''Return the number of leaves in a Phylo tree t.'''
num_terminals = lambda t: sum(1 for _ in t.get_terminals())

'''Return the split distance between two trees.'''
dist_split = lambda t1, t2, s: 2 * (num_terminals(t1) - 3 - len(tree_to_set(t1, s) & tree_to_set(t2, s)))

if __name__ == '__main__':
    # test_binary_search_tree()
    test_binary_tree()
