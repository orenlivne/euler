#!/usr/bin/env python
'''
============================================================
Sort file name strings representing chromosome chunks
first by chromosome, then by chunk.

chr(chr_number).(chunk_number).suffix

Usage:
python sort_chunk_names.py (reads strings from stdin)
python sort_chunk_names.py file name (reads strings from file_name)

Created on February 26, 2014
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys, re

'''A convenient cached regular expression of chunk file name strings.'''
CHUNK_NAME = re.compile('chr(\d+)\.(\d+)\..*')

def parse_chunk(s):
    '''Return the chromosome number and chunk number of the chunk file name string s.
    The returned tuple serves as a sorting key of chunk file name strings.'''
    m = re.match(CHUNK_NAME, s)
    return int(m.group(1)), int(m.group(2))

if __name__ == '__main__':
    try:
        input_file = open(sys.argv[1], 'rb') if len(sys.argv) == 2 else sys.stdin 
        for s in sorted(list(x.strip() for x in input_file), key=parse_chunk): print s
    except (IOError, OSError):
        sys.exit(141)