'''
============================================================
http://rosalind.info/problems/qrtd

Given: A list containing n taxa (n<=2000) and two unrooted
binary trees T1 and T2 on the given taxa. Both T1 and T2 are
given in Newick format.

Return: The quartet distance dq(T1,T2).
============================================================
'''
# From http://rosalind.info/problems/qrtd/solutions/.
# Need to get the rest of his libraries

import time
from rosalind import rostree

def qrtd(fp):
    taxa = next(fp).split()
    t1_str = next(fp)
    t2_str = next(fp)

    taxa_id = dict((s,i) for i, s in enumerate(taxa))
    all_taxa = set(xrange(len(taxa)))

    start_time = time.time()

    def build_tree(t_str):
        T = rostree.read_newick_str(t_str)
        #T = make_unrooted_binary(T)
        for node in T.walk(order=T.POSTORDER):
            if node.is_leaf:
                node.id = taxa_id[node.val]
                node.nodes = set([node.id])
                node.rest = all_taxa - node.nodes
            else:
                node.nodes = reduce(set.union, map(attrgetter('nodes'), node.children), set())
                node.rest = all_taxa - node.nodes

        # special case to walk unroot tree; the first node is also a leaf node
        T.id = taxa_id[T.val]
        T.nodes = set([T.id])
        T.rest = all_taxa - T.nodes
        return T

    T1 = build_tree(t1_str)
    T2 = build_tree(t2_str)

    # link T2 nodes to T1. Mind the special case for root node.
    id_2_T1 = dict((node.id,node) for node in T1.walk(type=T1.LEAF))
    id_2_T1[T1.id] = T1
    for node in T2.walk(type=T1.LEAF):
        node.t1_node = id_2_T1[node.id]
    T2.t1_node = id_2_T1[T2.id]

    N = len(taxa)
    print 'N=',N
    count = 0

    for i, v1 in enumerate(T1.walk(type=T1.INODE)):
        if v1 is T1:
            continue
        if i % 10 == 0:
            print 'T1 %3d %s' % (time.time() - start_time, i)
        for A_node in T1.walk(exclude_node=v1):
            A_node.color = 1
        for B_node in v1.left.walk():
            B_node.color = 2
        for C_node in v1.right.walk():
            C_node.color = 3

        A1 = v1.rest
        B1 = v1.left.nodes
        C1 = v1.right.nodes

        for v2 in T2.walk(order=T2.POSTORDER):
            if v2 is T2:
                pass
            elif v2.is_leaf:
                v2.a1 = 0
                v2.b1 = 0
                v2.c1 = 0
                c = v2.t1_node.color
                if    c == 1: v2.a1 = 1
                elif  c == 2: v2.b1 = 1
                else:         v2.c1 = 1
            else:
                B = v2.left
                C = v2.right

                a1b2 = B.a1
                a1c2 = C.a1
                a1a2 = len(A1) - a1b2 - a1c2
                b1b2 = B.b1
                b1c2 = C.b1
                b1a2 = len(B1) - b1b2 - b1c2
                c1b2 = B.c1
                c1c2 = C.c1
                c1a2 = len(C1) - c1b2 - c1c2

                # rememeber under v2, how many of them intersect with A1, B1 and C1
                v2.a1 = a1b2 + a1c2
                v2.b1 = b1b2 + b1c2
                v2.c1 = c1b2 + c1c2

                # 3x3=9 different orientation for T12 and T2,
                # times in each case two ways to pair B and C from each tree
                count += a1a2 * (a1a2-1) / 2 * (b1b2 * c1c2 + b1c2 * c1b2)
                count += a1b2 * (a1b2-1) / 2 * (b1a2 * c1c2 + b1c2 * c1a2)
                count += a1c2 * (a1c2-1) / 2 * (b1a2 * c1b2 + b1b2 * c1a2)
                count += b1a2 * (b1a2-1) / 2 * (a1b2 * c1c2 + a1c2 * c1b2)
                count += b1b2 * (b1b2-1) / 2 * (a1a2 * c1c2 + a1c2 * c1a2)
                count += b1c2 * (b1c2-1) / 2 * (a1a2 * c1b2 + a1b2 * c1a2)
                count += c1a2 * (c1a2-1) / 2 * (a1b2 * b1c2 + a1c2 * b1b2)
                count += c1b2 * (c1b2-1) / 2 * (a1a2 * b1c2 + a1c2 * b1a2)
                count += c1c2 * (c1c2-1) / 2 * (a1a2 * b1b2 + a1b2 * b1a2)

    print N * (N - 1) * (N- 2) * (N - 3) / 12 - count

if __name__ == "__main__":
    print qrtd('rosalind_qrtd_sample.dat')
    #print qrtd('rosalind_qrtd.dat')
