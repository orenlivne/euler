'''
============================================================
http://rosalind.info/problems/rsub

Given: A rooted binary tree T with labeled nodes in Newick
format, followed by a collection of at most 100 DNA strings
in FASTA format whose labels correspond to the labels of T.
We will assume that the DNA strings have the same length,
which does not exceed 400 bp).

Return: A list of all reversing substitutions in T (in any
order), with each substitution encoded by the following
three items:

the name of the species in which the symbol is first
changed, followed by the name of the species in which it
changes back to its original state the position in the
string at which the reversing substitution occurs; and
the reversing substitution in the form
original_symbol->substituted_symbol->reverted_symbol.
============================================================
'''
import rostree as rt
from Bio.SeqIO.FastaIO import FastaIterator 

# def reversing_subs(t, s):
#     '''Yield all reversing substitutions in the tuple format
#     ((start_node,sub_node1,sub_node2), (letter,new letter,letter)).'''
#     paths = {}
#     for node in t.find_clades(order='preorder'):
#         n = node.name
#         sn = s[n]
#         # q = dictionary of paths at node n. p = parent paths
#         # First, add new path starting at this node
#         q, p = {(n,): (sn,)}, paths[node.parent.name] if node.parent else {}
# #        print 'node', node.name, 'parent paths', q
#         for k, v in p.iteritems():  # Attempt to extend parent's paths
#             l = len(v)
#             if l == 1:
#                 if sn != v[0]:
#                     #print '\t', (k, v), 'extended to ', (k + (n,), v + (sn,))
#                     q[k + (n,)] = v + (sn,)  # T becomes T,G
# #                else:
# #                    print (k, v), 'deleted'
#             elif l == 2:
#                 if sn == v[0]:
# #                    print '\t', 'Found path', (k + (n,), v + (sn,))
#                     yield (k + (n,), v + (sn,))  # T,G becomes T,G,T. Emit and delete
#                 elif sn == v[1]: 
# #                    print '\t', (k, v), 'replacing sub ref ', (k[0], n), v
#                     q[(k[0], n)] = v  # T,G becomes T,G, update G's node reference
# #                else:
# #                    print '\t', (k, v), 'deleted'
#                     
#         paths[n] = q
# #    for n, q in paths.iteritems(): 
# #        print n, q

def is_sub(t, s, u):
    '''Yield all reversing substitutions in the tuple format
    ((sub_node,back_to_orig_node), (old letter,new letter)), if back_to_orig_node=u.
    Otherwise return None.'''
    v = u.parent
    #print 'u', u
    if v:
        su, sv, w = s[u.name], s[v.name], v
        #print 'v', v
        while w and s[w.name] == sv:
            #print 'w', w 
            w, w_child = w.parent, w
        #print 'Final w', w
        if w and s[w.name] == su: return ((w_child.name, u.name), (s[w_child.name], su))
    
def reversing_subs(t, s):
    '''Yield all reversing substitutions in the tuple format
    ((sub_node,back_to_orig_node), (old letter,new letter)).'''
    for u in t.find_clades():
        r = is_sub(t,s,u)
        if r: 
            #print r
            yield r

def rsub(file_name):
    '''Main driver to solve this problem.'''
    f = open(file_name, 'rb')
    t = rt.read_newick_str(f.readline().strip())
    s = dict((record.name, record.seq) for record in FastaIterator(f))
    # print s
    for i in xrange(len(next(s.itervalues()))):
#        print '-' * 70
#        print 'i', i
#        print '-' * 70
        si = dict((k, v[i]) for k, v in s.iteritems())
        for node, letter in reversing_subs(t, si):
            print '%s %s %d %s->%s->%s' % (node[0], node[1], i + 1, letter[1], letter[0], letter[1])

if __name__ == "__main__":
    #rsub('rosalind_rsub_sample.dat')
    rsub('rosalind_rsub.dat')
