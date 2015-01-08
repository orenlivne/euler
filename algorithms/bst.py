'''
============================================================
Binary Search Tree (BST).
============================================================
'''
class Node(object):
    '''A BST node.'''
    __slots__ = ('left', 'right', 'data')
    def __init__(self, left, right, data): self.left, self.right, self.data = left, right, data
    
class Bst(object):
    '''A Binary Search Tree (BST).'''
    def __init__(self, values=None):
        '''Create a tree. If values is a non-None iterable, its elements are inserted into the tree
        in iteration order.'''
        self.root = None
        if values:
            for data in values: self.insert(data)
        
    def insert(self, data):
        '''Insert an element into the tree.'''
        n = self.root
        if not n: self.root = Node(None, None, data)
        else:
            while True:
                if data <= n.data:
                    if not n.left:
                        n.left = Node(None, None, data)
                        break
                    else: n = n.left
                else:
                    if not n.right:
                        n.right = Node(None, None, data)
                        break
                    else: n = n.right

    '''Yield the elements of a BST in pre-traversal order.'''
    def preorder(self): return self.__preorder(self.root)
    '''Yield the elements of a BST in sorted order.'''
    def inorder(self): return self.__inorder(self.root)
    '''Yield the elements of a BST in post-traversal order.'''
    def postorder(self): return self.__postorder(self.root)

    def __preorder(self, n):
        '''Yield the elements of the subtree rooted at n in pre-traversal order.'''
        if not n: return
        yield n.data
        for data in self.__preorder(n.left): yield data
        for data in self.__preorder(n.right): yield data
    
    def __inorder(self, n):
        '''Yield the elements the subtree rooted at n in sorted order.'''
        if not n: return
        for data in self.__inorder(n.left): yield data
        yield n.data
        for data in self.__inorder(n.right): yield data
    
    def __postorder(self, n):
        '''Yield the elements the subtree rooted at n in post-traversal order.'''
        if not n: return
        for data in self.__postorder(n.left): yield data
        for data in self.__postorder(n.right): yield data
        yield n.data

    '''Yield the elements of a BST in pre-traversal order. No recursion'''
    def preorder_nr(self):
        stack = [self.root]
        while stack:
            n = stack.pop()
            if n:
                yield n.data
                stack.append(n.right)
                stack.append(n.left)

if __name__ == "__main__":
    b = Bst([100, 50, 150, 25, 75, 125, 175, 110])
    print list(b.preorder())
    print list(b.inorder())
    print list(b.postorder())

    print list(b.preorder_nr())
