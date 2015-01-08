'''
============================================================
Counting words in a file.
============================================================
'''
from __future__ import division
import itertools as it, re
from math import ceil
from collections import Counter
import time

'''Regular expression of English words.'''
WORD_PATTERN = re.compile('^([a-zA-Z]*)[\?|\!]*$')

def to_word(s):
    '''Split a hyphenated word into words. Remove capitalization, suffix symbols (exclamation, etc.)'''
    for word in s.split('-'):
        m = WORD_PATTERN.match(word.lower())
        if m: yield m.groups()[0]

words = lambda f: it.ifilter(lambda x: x, (word for line in f for s in line.split() for word in to_word(s)))

def column_format(entries, cols, delimiter='\t'):
    n = len(entries)
    col_size = int(ceil(n / cols))
    for j in xrange(col_size):
        for i in xrange(j, n, col_size):
            if i > j: print '%s' % (delimiter,),
            w, c = entries[i]
            print '%-10s %-5d' % (w, c),
        print ''
    
def print_top_entries(file_name, entries=21, cols=3):
    with open(file_name, 'rb') as f: column_format(Counter(words(f)).most_common(entries), 3)

def print_all_entries(file_name, cols=3):
    with open(file_name, 'rb') as f:
        for w, c in Counter(words(f)).iteritems(): print w, c

if __name__ == "__main__":
    print_top_entries('C:/Users/oren/Downloads/Bible/Bible.txt', entries=200)
