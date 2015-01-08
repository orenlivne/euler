'''
============================================================
http://rosalind.info/problems/mrna

Pitfalls of Reversing Translationclick to expand

Problem

For positive integers a and n, a modulo n (written amodn in shorthand) is the remainder when a is divided by n. For example, 29mod11=7 because 29=11x2+7.

Modular arithmetic is the study of addition, subtraction, multiplication, and division with respect to the modulo operation. We say that a and b are congruent modulo n if amodn=bmodn; in this case, we use the notation a=bmodn.

Two useful facts in modular arithmetic are that if a=bmodn and c=dmodn, then a+c=b+dmodn and axc=bxdmodn. To check your understanding of these rules, you may wish to verify these relationships for a=29, b=73, c=10, d=32, and n=11.

As you will see in this exercise, some Rosalind problems will ask for a (very large) integer solution modulo a smaller number to avoid the computational pitfalls that arise with storing such large numbers.

Given: A protein string of length at most 1000 aa.

Return: The total number of different RNA strings from which the protein could have been translated, modulo 1,000,000. (Don't neglect the importance of the stop codon in protein translation.)
============================================================
'''
import rosalind.rosutil as ro
from itertools import chain

INV_CODON = {}
for k, v in ro.RNA_TRANSLATION.iteritems(): INV_CODON.setdefault(v, []).append(k)

def mrna(s, r=1000000):
#    print [len(INV_CODON[x]) for x in chain(s, [STOP_VALUE])]
    return ro.prod_mod((len(INV_CODON[x]) for x in chain(s, [ro.STOP_VALUE])), r)

if __name__ == "__main__":
    print mrna(ro.read_str('rosalind_mrna_sample.dat'))
    print mrna(ro.read_str('rosalind_mrna.dat'))
        
