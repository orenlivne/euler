'''
============================================================
http://projecteuler.net/problem=265

2N binary digits can be placed in a circle so that all the N-digit clockwise subsequences are distinct.

For N=3, two such circular arrangements are possible, ignoring rotations:


For the first arrangement, the 3-digit subsequences, in clockwise order, are:
000, 001, 010, 101, 011, 111, 110 and 100.

Each circular arrangement can be encoded as a number by concatenating the binary digits starting with the subsequence of all zeros as the most significant bits and proceeding clockwise. The two arrangements for N=3 are thus represented as 23 and 29:

00010111_2 = 23
00011101_2 = 29
Calling S(N) the sum of the unique numeric representations, we can see that S(3) = 23 + 29 = 52.

Find S(5).
============================================================
'''
from itertools import imap

def all_paths(path, in_path, base):
    '''Return all paths from the node ''path'' to the leaves in the state tree. in_path is a
    constant-time -lookup boolean state array, indicating whether each of the numbers 0..2**n-1
    are in the path.'''
    if all(in_path): yield path  # path is a leaf node in the state tree
    last = path[-1]
    prefix = 2 * (last % base)
    for x in (x for x in (prefix, prefix + 1) if not in_path[x]):  # Look in all eligible branches
        in_path[x] = True  # Add x to path
        path.append(x)
        for p in all_paths(path, in_path, base): yield p  # Recursion
        in_path[x] = False  # Remove x from path
        path.pop()

'''Convert binary string to decimal.'''
dec = lambda x: int(x, 2)

'''Path code (circle path [0,0,0,1,0,1,1,1] -> 00010111_2 -> 23)'''
path_code = lambda path, base: dec(''.join(str(x / base) for x in path))

def S(n):
    '''Returns the sum of all path codes for length-n sequences.'''
    b = 2 ** (n - 1)
    return sum(imap(lambda x: path_code(x, b), all_paths([0], [True] + [False] * (2 * b - 1), b)))

if __name__ == "__main__":
    print S(3) # 5
    print S(5) # 209110240768
