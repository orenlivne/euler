'''
============================================================
http://projecteuler.net/problem=433
============================================================
'''
# Parallelizing the solution of ken, 25 Jun 2013 07:13 pm
# http://projecteuler.net/thread=433

import sys, time
from multiprocessing import Pool, Manager
#from euler.problem005 import gcd

def writeln(s, lock=None):
    if lock: lock.acquire()
    sys.stdout.write(s + '\n')
    sys.stdout.flush()
    if lock: lock.release()

def branch_sum((N, n, d, s, lock)):
    start_time = time.time()
    result, nodes = pair((N, n, d, s))
    writeln('branch (%d,%d) depth %d nodes %d time %.2f' % (n, d, s, nodes, time.time() - start_time), lock)
    return result

def pair((N, n, d, s)):
    print '\t' * s, s, (n, d), (N // d), 'x', (2 * s + 1)
    result, nodes = (N // d) * (2 * s + 1), 1
    for nn in xrange(n + d, N + 1, d):
        r, n = pair((N, d, nn, s + 1))
        result += r
        nodes += n 
    return result, nodes

def branches(N, n, d, s, s_max):
    br = [(n, d, s)]
    result = (N // d) * (2 * s + 1) if s < s_max else 0
    if s <= s_max:
        for nn in xrange(n + d, N + 1, d):
            r, b = branches(N, d, nn, s + 1, s_max)
            result += r
            br += b
    return result, br

def S(N): return pair((N, 1, 1, 0))[0]

def branches_at_depth(N, s_max):
    result, br = branches(N, 1, 1, 0, s_max)
    return result, [x for x in br if x[2] == s_max]

def S_branches(N, result, branches): return result + sum(pair((N, n, d, s))[0] for n, d, s in branches)

if __name__ == "__main__":
    manager = Manager()
    lock = manager.Lock()
    N, processes, depth = map(int, sys.argv[1:4])

    root_result, branches = branches_at_depth(N, depth)
    writeln('N %d processes %d branches %d' % (N, processes, len(branches)))
    
    pool = Pool(processes=processes)
    result = pool.map(branch_sum, [(N, n, d, s, lock) for n, d, s in branches])
    print sum(result) + root_result
