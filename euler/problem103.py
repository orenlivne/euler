'''
============================================================
http://projecteuler.net/problem=103

============================================================
'''
from problem106 import valid_pairs
from problem105 import I_holds
from math import ceil

def min_special_sum7(M=100):
    S, A, pairs, done = 0, [], list(valid_pairs(7)), False
    for a1 in xrange(10, M):  # it.count(10):
        if S and a1 >= (S - 18) / 6.: break
        #print 'a1', a1
        for a2 in xrange(a1 + 1, M):  # it.count(a1 + 1):
            #print 'a1', a1, 'a2', a2
            if S and a2 >= (S - 15) / 6.:
                done = True
                break
            for a3 in xrange(a2 + 1, min(M, a1 + a2 - 8)):
                for a4 in xrange(a3 + 1, min(M, int(ceil((a1 + a2 + a3) / 2.)) - 3)):
                    for a5 in xrange(a4 + 1, min(M, int(ceil((a1 + a2 + a3 + a4) / 3.)) - 1)):
                        for a6 in xrange(a5 + 1, min(M, int(ceil((a1 + a2 + a3 + a4 - a5 - 1) / 2.)))):
                            for a7 in xrange(a6 + 1, min(M, a1 + a2 + a3 + a4 - a5 - a6)):
                                #print '\t\t', (a3 + 1, int(ceil((a1 + a2 + a3) / 2.)) - 3), (a3 + 1, int(ceil((a1 + a2 + a3) / 2.)) - 3), (a4 + 1, int(ceil((a1 + a2 + a3 + a4) / 3.)) - 1), (a5 + 1, int(ceil((a1 + a2 + a3 + a4 - a5 - 1) / 2.))), (a6 + 1, a1 + a2 + a3 + a4 - a5 - a6)
                                a = (a1, a2, a3, a4, a5, a6, a7)
                                if I_holds(a, pairs):
                                    Sa = sum(a)
                                    #print a, Sa
                                    if S == 0 or Sa < S: S, A = Sa, a
        if done: break
    return ''.join(map(str, A))

if __name__ == "__main__":
    print min_special_sum7()
