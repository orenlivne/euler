'''
============================================================
http://rosalind.info/problems/seto

Given: A positive integer n (n<=20,000) and two subsets A and B of {1,2,...,n}.

Return: Six sets: A U B, A CAP B, A-B, B-A, Ac, and Bc (where set complements are taken with respect to {1,2,...,n}).
============================================================
'''
import rosalind.rosutil as ro

def seto(f):
    lines = list(ro.read_lines(f))
    n, a, b = int(lines[0]), ro.read_int_set(lines[1]), ro.read_int_set(lines[2])
    u = set(range(1, n + 1))
    print '\n'.join(map(ro.repr_set, (a | b, a & b, a - b, b - a, u - a, u - b)))
    
if __name__ == "__main__":
    #seto('rosalind_seto_sample.dat')
    seto('rosalind_seto.dat')
