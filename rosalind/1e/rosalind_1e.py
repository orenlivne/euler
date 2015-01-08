'''
============================================================
http://rosalind.info/problems/1e

Define the skew of a DNA string Genome, denoted Skew(Genome), as the difference between the total number of occurrences of G and C in Genome. Let Prefixi (Genome) denote the prefix (i.e., initial substring) of Genome of length i. For example, the values of Skew(Prefixi ("CATGGGCATCGGCCATACGCC")) are:

0 -1 -1 -1 0 1 2 1 1 1 0 1 2 1 0 0 0 0 -1 0 -1 -2
============================================================
'''
import rosalind.rosutil as ro

def prefix_skew(s):
    '''A generator of skews of all of s\'s prefixes.'''
    b = 0
    yield b  # The empty prefix
    for x in s:
        if x == 'G': b += 1
        elif x == 'C': b -= 1
        yield b

def prefix_skew_argmax(s):
    p = list((v, k) for k, v in enumerate(prefix_skew(s)))
    v_max = min(p)[0]
    return [k for v, k in p if v == v_max]

def one_e(f):
    return ro.join_list(prefix_skew_argmax(ro.read_str(f)))

if __name__ == "__main__":
    print one_e('rosalind_1e_sample.dat')
    print one_e('rosalind_1e.dat')