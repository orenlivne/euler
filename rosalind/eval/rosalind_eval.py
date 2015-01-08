'''
============================================================
http://rosalind.info/problems/eval

Say that you place a number of bets on your favorite sports teams. If their chances of winning are 0.3, 0.8, and 0.6, then you should expect on average to win 0.3 + 0.8 + 0.6 = 1.7 of your bets (of course, you can never win exactly 1.7!)

More generally, if we have a collection of events A1,A2,...,An, then the expected number of events occurring is Pr(A1)+Pr(A2)+...+Pr(An) (consult the note following the problem for a precise explanation of this fact). In this problem, we extend the idea of finding an expected number of events to finding the expected number of times that a given string occurs as a substring of a random string.

Given: A positive integer n (n<=1,000,000), a DNA string s of even length at most 10, and an array A of length at most 20, containing numbers between 0 and 1.

Return: An array B having the same length as A in which B[i]
represents the expected number of times that s will appear as
a substring of a random DNA string t of length n, where t is
formed with GC-content A[i] (see "Introduction to Random
Strings").
============================================================
'''
import rosalind.rosutil as r

g = lambda n, s, x: pow(0.5 * x, r.gc_count(s)) * pow(0.5 * (1 - x), len(s) - r.gc_count(s)) * (n - len(s) + 1)

def roseval(file_name):
    with open(file_name, 'rb') as f:
        n = int(f.next())
        s = f.next().strip()
        return ' '.join(repr(g(n, s, float(x))) for x in f.next().split())
               
if __name__ == "__main__":
    print roseval('rosalind_eval_sample.dat')
    print roseval('rosalind_eval.dat')
