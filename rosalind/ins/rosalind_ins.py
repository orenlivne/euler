'''
============================================================
http://rosalind.info/problems/ins

Insertion sort is a simple algorithm with quadratic running
time that builds the final sorted array one item at a time.

Given: A positive integer n<=10**3 and an array A[1..n] of
integers.

Return: The number of swaps performed by insertion sort
algorithm on A[1..n].

Discussion

For this problem, it is enough to implement the pseudocode
above with a quadratic running time and to count the number
of swaps performed. Note however that there exists an
algorithm counting the number of swaps in O(nlogn).

Note also that Insertion Sort is an in-place algorithm as it
only requires storing a few counters.
============================================================
'''
import rosalind.rosutil as ro, numpy as np
from pybst.rbtree import RBTree
from numpy.ma.testutils import assert_equal

# Fast impl broken... wrong count updates???????

class RBTreeAug(RBTree):
    '''Augmented RBTree instance t with additional properties at each node:
    * \'count\' = #nodes in the node\'s-subtree.'''

    def __init__(self, *args):
        RBTree.__init__(self, *args)
        # Augment all nodes with counts
        if self.get_element_count():
            for node in self.postorder(): node.count = RBTreeAug.__count(node)

    def insert_aug(self, key, value, *args):
        self.insert(key, value, *args)
        #print 'insert_aug(%d)' % (key,)
        
        # Increment counts of nodes on the path from new node root
        node = self.get_node(key)
        node.count = 1

        node = node.parent
        while node:
            #print 'Updating node', node.key, 'current count', node.count
            node.count += 1
            node = node.parent
        
    def count(self):
        return dict((node.key, node.count) for node in self.postorder())
     
    @staticmethod
    def __count(node):
        '''#nodes in the node\'s-subtree. Works only in post-traversal order.'''
        return 1 + (0 if not node.left and not node.right else (node.left.count if node.left else 0) + (node.right.count if node.right else 0))

def rank(t, x):
    '''Return the order statistic (0-based rank) of x in the count-augmented RBTree t.'''
    node, offset = t.Root, 0
    while node:
        if x < node.key: node = node.left
        elif x == node.key: return offset + (node.left.count if node.left else 0)
        else: node, offset = node.right, offset + (node.left.count if node.left else 0) + 1
    raise ValueError('Element not found')

def num_swaps(a):
    '''#Swaps in insertion sort of a.'''
    n, t = len(a), RBTreeAug()
    print a
    s = n * (n - 1) / 2
    for x in a:
        t.insert_aug(x, None)
        #print x, rank(t, x), t.count()
        s -= rank(t, x)
    return s
    
def ins(f):
    '''Main driver to solve this problem.'''
    return num_swaps_bf(ro.to_int_list(ro.read_lines(f)[1]))

def num_swaps_bf(a):
    '''#Swaps in insertion sort of a. O(n^2) impl.'''
    s = 0
    for i in xrange(1, len(a)):
        k = i
        while k > 0 and a[k] < a[k - 1]:
            a[k], a[k - 1], k, s = a[k - 1], a[k], k - 1, s + 1
    return s
    
def test_rank():
    a = [6, 10, 4, 5, 1, 2]
    t = RBTreeAug((k, k) for k in a)
    assert_equal([rank(t, x) for x in a], np.argsort(a))  

def test_ins(f):
    a = ro.to_int_list(ro.read_lines(f)[1])
    print num_swaps_bf(a)  # .copy()
    print num_swaps(a) 
          
if __name__ == "__main__":
    test_rank()
    print ins('rosalind_ins_sample.dat')
    print ins('rosalind_ins.dat')
    #test_ins('rosalind_ins_sample.dat')
    # test_ins('rosalind_ins.dat')
