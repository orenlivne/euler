'''
============================================================
Implement an algorithm to print all possible valid 
combinations of braces when n pairs of paranthesis are
given. 
============================================================
'''
'''Generate all legal combinations of n parentheses pairs as binary sequences.'''
paren = lambda n: _paren(1, 1, n, n - 1)  # Start a state tree search at the root node containing one left parentheses = one 1

def _paren(s, balance, c0, c1):
    '''A recursive helper function. Searches the subtree of s = root node''s binary sequence;
    balance = #1's - #0's in s; c0 = #0's remaining; c1 = #1's remaining. Complexity: O(2^(2n)).'''
    if c0 == 0 and c1 == 0:  # Dispensed exactly all paren pairs, emit string. This is a leave node.
        yield s
        return
    if c0 > 0 and balance > 0:  # We have a 0 left and there are more 1's than 0's in the string, dispense a 0 (=search in left sub-tree) 
        for x in _paren(s << 1, balance - 1, c0 - 1, c1): yield x
    if c1 > 0:  # We have a 1 left. We can always use a 1 regardless of the #0s. Dispense a 1 (=search in right sub-tree) 
        for x in _paren((s << 1) + 1, balance + 1, c0 , c1 - 1): yield x

'''Dictionary that converts bits to parenthesis strings.'''    
PAREN = (')', '(')
'''Generate all legal combinations of n parentheses pairs as parenthesis sequence strings.'''
paren_str = lambda n: (''.join(map(PAREN.__getitem__, map(int, bin(s)[2:]))) for s in paren(n))

if __name__ == "__main__":
    for k, x in enumerate(list(paren_str(5)), 1):
        print k, x
    for n in xrange(1, 12): print n, sum(1 for _ in paren_str(n))
