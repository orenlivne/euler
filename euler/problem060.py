'''
============================================================
http://projecteuler.net/problem=60

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order the result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four primes, 792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.
============================================================
'''
import itertools as it
from problem007 import primes
from problem037 import is_prime
from euler.problem012 import Primes

#--------------------------------------------
# Plain brute-force solution
#--------------------------------------------
def concate_set_brute_force(k, n_max, S_initial=list()):
    '''Min sum concat prime set of size k whose elements < n_max.'''
    S_min, s_min = None, 0
    for S in it.ifilter(is_concat_set, (S_initial + list(x) for x in it.combinations(primes('lt', n_max), k - len(S_initial)))):
        # print '\t', S
        s = sum(S)
        if S_min is None or s < s_min:
            S_min, s_min = S, s
    return S_min

'''Concatenate the numbers a,b.'''
concat = lambda a, b: int(str(a) + str(b))

def is_concat_set(S):
    for a, b in it.combinations(S, 2):
        # print '\t', concat(a, b), concat(b, a), is_prime(concat(a, b)), is_prime(concat(b, a))
        if not is_prime(concat(a, b)) or not is_prime(concat(b, a)):
            return False
    return True

#--------------------------------------------
# Stack solution
#--------------------------------------------
'''x,y = prime strings. Is the pair x,y valid?'''
valid_pair = lambda x, y: is_prime(int(x + y)) and is_prime(int(y + x))

def valid_seq(a):
    '''Assuming a[:-1] is a valid seq, is a valid?'''
    x = str(a[-1])
    return all(valid_pair(x, str(y)) for y in a[:-1])

def _min_sum(k, num_primes):
    '''Return the min k-seq sum (k>=2). Search among the first num_primes (>=2) primes.'''
    p = primes('first', num_primes)[1:]  # Exclude 2 since we know it cannot be in a valid sequence
    a, d, smin, N, min_d = [0], 1, 0, len(p), 0  # a contains indices into p
    min_pa = []
    print 'N', N
    while True:
        pa = [p[x] for x in a]
        valid = valid_seq(pa)
        # print 'a', a, 'seq', pa, 'valid?', valid
        if valid:
            if d == k:  # Found new candidate for min seq
                s = sum(pa)
                if smin == 0 or s < smin:
                    smin, min_pa = s, pa
                    print 'Valid sequence: ', s, pa
                a[-1] += 1  # Advance to next number at same depth
            else:
                a.append(a[-1] + 1)  # Increase depth
                d += 1
        else:
            a[-1] += 1
        
        # print 'New a', a, 'smin', smin
        # Advance to next seq 
        while d > min_d:
            # print '\t', a
            x = a[-1]
            if x == N or (smin > 0 and (sum(p[x] for x in a) >= smin if d == k else  
                                        (x >= (smin - sum(p[x] for x in a) - 0.5 * (k - d - 1)) / (k - d)))):
                x = a.pop()
                d -= 1
                if d > min_d:
                    a[-1] += 1
            else:
                break
        if d == min_d + 1:
            if a[0] % 10 == 0:
                print 'Starting at', p[a[0]]
        if d == min_d:
            # Exhausted search space
            break
    return smin, min_pa

#--------- piro's solution 2008 ------
# map each n into the list of compatible numbers < n
pmap = {}

def solve_p060(size):
    for n in Primes():
        sn = str(n)
        pp = []
        for p in pmap:
            if is_prime(int(sn + p)) and is_prime(int(p + sn)):
                pp.append(p)
        pmap[sn] = set(pp)
        
        for sol in iter_sol(sn, size):
            print ', '.join(sol)
            return sum(map(int, sol))

# Cache: for each solution length, the corresponding value in this map is the
# set of numbers x for which there is no solution of this length with whose biggest number is x 
noway = {}

def iter_sol(sn, length):
    """Get solutions of the proper length having sn as biggest number."""
    if length == 1:
        yield (sn,)
        return

    if length not in noway:
        noway[length] = set()

    if sn in noway[length]:
        return

    found = False
    pmap_sn = pmap[sn]
    for sol in it.chain(*(it.ifilter(lambda sol: all(p2 in pmap_sn for p2 in sol), 
                                     iter_sol(p, length - 1)) for p in pmap_sn)):
        yield sol + (sn,)
        found = True

    if not found:
        noway[length].add(sn)

def min_sum(k):
    return it.dropwhile(lambda x: x[0] == 0, (_min_sum(k, 10 * 2 ** n) for n in it.count())).next()
    
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
#     print concate_set_brute_force(2, 150)
#     print concate_set_brute_force(3, 150)
#     # print concate_set_brute_force(4, 1000)
#     # print concate_set_brute_force(5, 10000, [3, 7])
# 
#     print min_sum(2)
#     print min_sum(3)
#     print min_sum(4)
#     print min_sum(5)

    print solve_p060(4)  # 792
    print solve_p060(5)  # 26033
