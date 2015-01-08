'''
============================================================
http://rosalind.info/problems/1d

Find patterns forming clumps in a string.

Given: A string Genome, and integers k, L, and t.

Return: All distinct k-mers forming (L, t)-clumps in Genome.
============================================================
'''
import rosalind.rosutil as ro

def shortest_clump(ind, t):
    return min(ind[i + t - 1] - ind[i] + 1 for i in xrange(len(ind) - t + 1))

def clumps(s, k, L, t):
    candidates = [x for x, v in ro.kmer_counter(s, k).iteritems() if v >= t]
    return (x for x in candidates if shortest_clump(list(ro.find_all(s, x)), t) <= L)

def one_d(f):
    lines = ro.read_lines(f)
    s = lines[0]
    k, L, t = map(int, lines[1].split())
    return ' '.join(clumps(s, k, L, t))

if __name__ == "__main__":
    print one_d('rosalind_1d_sample.dat')
    print one_d('rosalind_1d.dat')
    