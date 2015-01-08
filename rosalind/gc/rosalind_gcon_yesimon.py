#!/usr/bin/env python
'''
============================================================
For validation of our GCON problem solution.

From https://github.com/yesimon/rosalind/blob/master/GCON.py

Created on Dec 29, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import rosalind.rosutil as ro, numpy as np
from itertools import product
from Bio.SubsMat.MatrixInfo import blosum62

def gcon_yesimon(f):
    x, y = ro.fafsa_values(f)
    return optimal_alignment_yesimon(x, y, -5)

def gaff_yesimon(f):
    x, y = ro.fafsa_values(f)
    return optimal_alignment_gaff_yesimon(x, y)

def gaff_burschka(f):
    x, y = ro.fafsa_values(f)
    return optimal_alignment_gaff_burschka(x, y, -11, -1)

# def gaff_kobak(f):
#     x, y = ro.fafsa_values(f)
#     score, augmDna1, augmDna2 = optimal_alignment_gaff_kobak(dnas[0], dnas[1], -11, -1)
#     print(score)
#     print(augmDna1)
#     print(augmDna2)    

def blosum62_score(x, y):
    cost = blosum62.get((x, y))
    if cost == None: cost = blosum62.get((y, x))
    return cost

def Global_Alignment_Affine_Gap(x , y , c=11 , l=1):

    m = len(x)
    n = len(y)

    A = np.zeros((m + 1 , n + 1) , dtype=np.int32)
    B = np.zeros((m + 1 , n + 1) , dtype=np.int32)

    A[:, 0] = -2 ** 31
    A[0, :] = -2 ** 31

    B[:, 0] = -2 ** 31
    B[0, :] = -2 ** 31

    GA = np.zeros((m + 1 , n + 1) , dtype=np.int32)

    GA[:, 0] = -c - l * np.arange(m + 1)
    GA[0, :] = -c - l * np.arange(n + 1)

    GA[0, 0] = 0

    for i in range(1 , m + 1) :
        for j in range(1 , n + 1):

            A[i, j] = np.max([ A[i - 1, j] - l , GA[i - 1, j] - c - l ])
            B[i, j] = np.max([ B[i, j - 1] - l , GA[i, j - 1] - c - l ])

            GA[i, j] = np.max([ A[i, j] ,
                                B[i, j] ,
                                GA[i - 1, j - 1] + blosum62_score(x[i - 1] , y[j - 1]) ])

    return GA[m, n]

# def optimal_alignment_gaff_kobak(seq1, seq2, openingPenalty, extensionPenalty):
#     NegInf = -10 ** 10
# 
#     score = [[0] + [openingPenalty + extensionPenalty * t for t in list(range(len(seq1)))]]
#     scoreVer = [[None] + [NegInf for t in list(range(len(seq1)))]]
#     scoreHor = [[None] * (len(seq1) + 1)]
#     scoreSub = [[None] * (len(seq1) + 1)]
# 
#     for j, s in enumerate(seq2):
#         scoreSub[-1].append(score[-2][i] + blosum62[(s, t)])
#         scoreHor[-1].append(max(scoreHor[-1][-1] + extensionPenalty, score[-1][-1] + openingPenalty))
#         scoreVer[-1].append(max(scoreVer[-2][i + 1] + extensionPenalty, score[-2][i + 1] + openingPenalty))
#         score[-1].append(max(scoreHor[-1][-1], scoreVer[-1][-1], scoreSub[-1][-1]))
# 
#         for i, t in enumerate(seq1):
#             scoreSub[-1].append(score[-2][i] + blosum62[(s, t)])
#             scoreHor[-1].append(max(scoreHor[-1][-1] + extensionPenalty, score[-1][-1] + openingPenalty))
#             scoreVer[-1].append(max(scoreVer[-2][i + 1] + extensionPenalty, score[-2][i + 1] + openingPenalty))
#             score[-1].append(max(scoreHor[-1][-1], scoreVer[-1][-1], scoreSub[-1][-1]))
# 
#     augmentedseq1, augmentedseq2 = '', ''
#     i, j = len(seq2), len(seq1)
#     while i >= 1 or j >= 1:
#         if score[i][j] == scoreSub[i][j]:
#             augmentedseq1 = seq1[j - 1] + augmentedseq1
#             augmentedseq2 = seq2[i - 1] + augmentedseq2
#             i -= 1
#             j -= 1
#         elif score[i][j] == scoreVer[i][j] or j == 0:
#             augmentedseq1 = '-' + augmentedseq1
#             augmentedseq2 = seq2[i - 1] + augmentedseq2
#             i -= 1
#         elif score[i][j] == scoreHor[i][j] or i == 0:
#             augmentedseq1 = seq1[j - 1] + augmentedseq1
#             augmentedseq2 = '-' + augmentedseq2
#             j -= 1
#         else:
#             print('Oops...')
#             break
# 
#     return score[-1][-1], augmentedseq1, augmentedseq2

def optimal_alignment_gaff_burschka(x, y, GAPO, GAPE):
    M = [[0] * len(y) for i in x]
    M[0][0] = max(blosum62_score(x[0], y[0]), GAPO + GAPE)
    for i in range(1, len(x)):
        M[i][0] = GAPO + max(GAPE * i + blosum62_score(x[i], y[0]), max(GAPE * (i - i2) + M[i2][0] for i2 in range(i)))
    for j in range(1, len(y)):
        M[0][j] = GAPO + max(GAPE * j + blosum62_score(x[0], y[j]), max(GAPE * (j - j2) + M[0][j2] for j2 in range(j)))
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            M[i][j] = max(
                blosum62_score(x[i], y[j]) + M[i - 1][j - 1],
                GAPO + max(GAPE * (i - i2) + M[i2][j] for i2 in range(i)),
                GAPO + max(GAPE * (j - j2) + M[i][j2] for j2 in range(j))
            )
    # print("\n".join(" ".join("% 3d" % i for i in row) for row in M))
    return M[-1][-1]

def optimal_alignment_yesimon(s, t, gap):
    sl, tl, m, f, g, h = len(s), len(t), {(0, 0): (0, None)}, {}, {}, {}
    m.update({((i, 0), (gap, (i - 1, 0))) for i in range(1, sl + 1)})
    m.update({((0, i), (gap, (0, i - 1))) for i in range(1, tl + 1)})
    for i, j in product(range(1, sl + 1), range(1, tl + 1)):
        f[(i, j)] = m[(i - 1, j - 1)][0] + blosum62_score(s[i - 1], t[j - 1])
        g[(i, j)] = max(m[(i - 1, j)][0] + gap, g.get((i - 1, j)))
        h[(i, j)] = max(m[(i, j - 1)][0] + gap, h.get((i, j - 1)))
        v = max(f[(i, j)], g[(i, j)], h[(i, j)])
        if v == f[(i, j)]: m[(i, j)] = (v, (i - 1, j - 1))
        elif v == g[(i, j)]: m[(i, j)] = (v, (i - 1, j))
        elif v == h[(i, j)]: m[(i, j)] = (v, (i, j - 1))
    return m[(i, j)][0]

def optimal_alignment_gaff_yesimon(s, t, gap_init= -11, gap_ext= -1):
    sl, tl = len(s), len(t)
    if sl < tl:
        return optimal_alignment_gaff_yesimon(t, s, gap_init, gap_ext)
    m = {(0, 0): (0, None)}
    f = {}
    g = {}
    h = {}
    m.update({((i, 0), (gap_init + gap_ext * (i - 1), (i - 1, 0))) for i in range(1, sl + 1)})
    m.update({((0, i), (gap_init + gap_ext * (i - 1), (0, i - 1))) for i in range(1, tl + 1)})
    for i, j in product(range(1, sl + 1), range(1, tl + 1)):
        cost = blosum62.get((s[i - 1], t[j - 1]))
        if cost == None:
            cost = blosum62.get((t[j - 1], s[i - 1]))
        f[(i, j)] = m[(i - 1, j - 1)][0] + cost
        gg = g.get((i - 1, j))
        if gg != None:
            gg += gap_ext
        hh = h.get((i, j - 1))
        if hh != None:
            hh += gap_ext
        g[(i, j)] = max(m[(i - 1, j)][0] + gap_init, gg)
        h[(i, j)] = max(m[(i, j - 1)][0] + gap_init, hh)
        v = max(f[(i, j)], g[(i, j)], h[(i, j)])
        if v == f[(i, j)]: m[(i, j)] = (v, (i - 1, j - 1))
        elif v == g[(i, j)]: m[(i, j)] = (v, (i - 1, j))
        elif v == h[(i, j)]: m[(i, j)] = (v, (i, j - 1))
    retval = m[(i, j)]
    print sl, tl
    for i in xrange(sl + 1):
        for j in xrange(tl + 1):
            print m[(i, j)] if (i, j) in m else '-',
        print
    print m
    return retval
    
if __name__ == '__main__':
    print gcon_yesimon('rosalind_gcon.dat')
