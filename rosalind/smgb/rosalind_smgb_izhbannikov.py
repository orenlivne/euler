'''
============================================================
http://rosalind.info/problems/smgb

For validation, from
https://bitbucket.org/izhbannikov/rosalind/raw/914551909d7698ab4d99b907a9fa12d9e4e2ed80/smgb/smgb.py
============================================================
'''
import rosalind.rosutil as ro, numpy as np, time
from Bio import SeqIO

match_award = 1
mismatch_penalty = -1
gap_penalty = -1 

# Print traceback matrix as a table:
def print_matrix():
    pass
#     print "    *",
#     for j in xrange(len(seq1)):
#         print " ", seq1[j],
#     print
#      
#     for i in xrange(len(seq2)+1):
#         print ("*" if i==0 else seq2[i-1]),
#         for j in xrange(len(seq1)+1):
#             print "%3d" % pointer[i][j],
#         print
#     print
#     
#     # Print scoring matrix
#     print "    *",
#     for j in xrange(len(seq1)):
#         print " ", seq1[j],
#     print
#      
#     for i in xrange(len(seq2)+1):
#         print ("*" if i==0 else seq2[i-1]),
#         for j in xrange(len(seq1)+1):
#             print "%3d" % score[i][j],
#         print
#      
#     #i = max_i
#     #j = max_j # indices of path starting point
    

# Creates empty matrix with all zeros
zeros = lambda m, n: [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]

# No substituition matrix, just simple linear gap penalty model
def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def nw(seq1, seq2):
    m, n = len(seq1), len(seq2)  # lengths of two sequences
    
    # Generate DP (Dynamic Programmed) table and traceback path pointer matrix
    score = zeros(n + 1, m + 1)  # the DP table
    for i in xrange(n + 1): score[i][0] = i * 0
    for j in xrange(m + 1): score[0][j] = j * 0
    
    # Traceback matrix
    pointer = zeros(n + 1, m + 1)  # to store the traceback path
    for i in xrange(n + 1): pointer[i][0] = 1
    for j in xrange(m + 1): pointer[0][j] = 2
    
    # Calculate DP table and mark pointers
    print m, n
    start = time.time()
    for i in xrange(1, n + 1):
        if i % 100 == 0: print i, time.time() - start
        for j in xrange(1, m + 1):
            score_diagonal = score[i - 1][j - 1] + match_score(seq1[j - 1], seq2[i - 1])
            score_up = score[i][j - 1] + gap_penalty
            score_left = score[i - 1][j] + gap_penalty
            s = max(score_left, score_up, score_diagonal)
            if s == score_diagonal: p = 3  # 3 means trace diagonal
            if s == score_up: p = 2  # 2 means trace left
            if s == score_left: p = 1  # 1 means trace up
            score[i][j] = s
            pointer[i][j] = p  
    align1, align2 = '', ''  # initial sequences
    max_j = score[-1].index(max(score[-1]))
    print max(score[-1])
    
    # Traceback from bottom right corner; i,j already set to this value after the previous loop,
    # follow pointers in the traceback matrix
    while i > 0 or j > 0:
        if j > max_j :
            align1 = seq1[j - 1] + align1
            align2 = '-' + align2
            j -= 1
            continue
        p = pointer[i][j]
        if p == 3 :  # 2 means trace diagonal
            align1 = seq1[j - 1] + align1
            align2 = seq2[i - 1] + align2
            i -= 1
            j -= 1
        elif p == 2 :  # 2 means trace left
            align1, align2, j = seq1[j - 1] + align1, '-' + align2
        elif p == 1 :  # 1 means trace up
            align1, align2, i = '-' + align1, seq2[i - 1] + align2, i - 1
    print align1 + '\n' + align2
    
if __name__ == "__main__":
    # Two sequences you want to align
    records = list(SeqIO.parse("rosalind_smgb.dat", "fasta"))
    seq11 = records[0].seq
    seq22 = records[1].seq

    # seq11 = "CAGCACTTGGATTCTCGG" 
    # seq22 = "CAGCGTGG"

    nw(seq11, seq22)
