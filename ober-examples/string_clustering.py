#!/usr/bin/env python
'''
============================================================
String clustering using thresholding on the similarity
matrix of word-level Dice distance.

Created on July 9, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, networkx as nx, re, sys

'''Tokenize a string into words.'''
words = lambda txt: set(re.findall(r'(?ms)\W*(\w+)', txt.lower()))
'''Calculate the Dice index between two bags of strings.'''
dice_distance = lambda g1, g2: (2.0 * len(g1 & g2)) / (len(g1) + len(g2))
'''Calculate the word-level Dice distanec between two strings.'''
dice_words = lambda s1, s2: dice_distance(words(s1), words(s2))
    
'''Main program'''
if __name__ == '__main__':
    # Read strings from stdin
    strings = map(lambda x: x.rstrip('\r\n').rstrip('\n').strip(), sys.stdin.readlines())
    
    # Calculate similarity matrix
    similarity = np.array([[dice_words(s, t) for t in strings] for s in strings])
    # Calculate blocks = connected components of thresholded matrix
    threshold = 0.75  # Arbitrary; seems to work for the disease name data set in question
    blocks = [sorted(block) for block in nx.connected_components(nx.from_edgelist(zip(*np.where(similarity > threshold)), nx.Graph()))]
    
    # For each string in the original list, write its block number, the string, and the standardized string
    # of the block to stdout, separated by commas
    for k, i, standard_i in ((k, i, block[0]) for k, block in enumerate(blocks, 1) for i in block):
        print "%d,%s,%s" % (k, strings[i], strings[standard_i])
