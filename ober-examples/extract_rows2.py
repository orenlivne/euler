#!/usr/bin/env python
'''
============================================================
Extract a subset of rows from a file whose numbers are
read from an index file.

Created on Jun 28, 2012
Tab-delimited, stdin support on July 2, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys, csv, os
from optparse import OptionParser

def select_rows(in_file, index):
    '''Output files from in_file whose lines are the numbers listed in index_file.'''
    # Get the first line number in the index
    next_num = int(index.next())
    if not next_num:
        raise StopIteration()

    # Loop over in_file lines until we reach the current index line
    for num, line in enumerate(in_file):
        if num == next_num:
            yield line
            # Go to next index line number
            next_num = int(index.next())
            if not next_num:
                raise StopIteration()

if __name__ == '__main__':
    '''
    --------------------------------------------------
    Main program
    --------------------------------------------------
    '''
    # Parse command-line arguments
    prog = os.path.basename(sys.argv[0])
    usage = 'Usage: %s <index-file>\n\n' \
        'Extract rows from standard input whose 0-based numbers are listed in a sorted index-file.\n\n' \
        'Type ''%s -h'' to display full help.' % (prog, prog)

    parser = OptionParser(usage=usage)
#    parser.add_option('-i', '--index-file', type='str'  , dest='index_file',
#                      default=None, help='If specified, outputs only the IDs listed in this file (these are indices between 0 and #ids-1, if the input file has #ids genotype columns)')
    (options, args) = parser.parse_args(sys.argv[1:])
    if len(args) != 1:
        print usage
        sys.exit(1)

    for row in select_rows(sys.stdin, open(args[0], 'rb')):
        sys.stdout.write(row)
