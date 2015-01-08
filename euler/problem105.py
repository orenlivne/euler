'''
============================================================
http://projecteuler.net/problem=105

Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:

S(B)  S(C); that is, sums of subsets cannot be equal.
If B contains more elements than C then S(B)  S(C).
For example, {81, 88, 75, 42, 87, 84, 86, 65} is not a special sum set because 65 + 87 + 88 = 75 + 81 + 84, whereas {157, 150, 164, 119, 79, 159, 161, 139, 158} satisfies both rules for all possible subset pair combinations and S(A) = 1286.

Using sets.txt (right click and "Save Link/Target As..."), a 4K text file with one-hundred sets containing seven to twelve elements (the two examples given above are the first two sets in the file), identify all the special sum sets, A1, A2, ..., Ak, and find the value of S(A1) + S(A2) + ... + S(Ak).

NOTE: This problem is related to problems 103 and 106.
============================================================
'''
from problem106 import valid_pairs

I_holds = lambda a, pairs: all(sum(a[i] for i in x) != sum(a[i] for i in y) for x, y in pairs)
II_holds = lambda a, n: sum(a[n - n / 2:]) < sum(a[:n / 2 + 1])

def special_sets(sets):
    '''An iterator of special-sum sets among the iterates of the iterator sets.'''
    pairs_dict = {}
    for a in sets:
        n = len(a)
        pn = pairs_dict.setdefault(n, list(valid_pairs(n)))
        if II_holds(a, n) and I_holds(a, pn): yield a

if __name__ == "__main__":
    print sum(sum(a) for a in special_sets(sorted(map(int, x.rstrip('\r\n').rstrip('\n').split(','))) for x in open('problem105.dat', 'rb')))
