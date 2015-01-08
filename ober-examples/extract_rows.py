#!/usr/bin/env python
'''
============================================================
Extract a subset of genomic data from standard input
by SNP and selected columns. Supports tab-delimited files.

Created on Jun 28, 2012
Tab-delimited, stdin support on July 2, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys, csv, os
from optparse import OptionParser

def __get_columns(separator, snp, columns, num_header_lines):
    '''Read the first two columns in a data file.'''
        # Read delimited data from standard input
    reader = csv.reader(sys.stdin, delimiter=separator, skipinitialspace=True)
    # Skip the first n lines
    for line in xrange(0, num_header_lines):
        reader.next()

    # Extract requested columns from relevant lines
    for line in reader:
        if line: # Make sure there's at least one entry
            if (line[0] == snp):
                yield tuple([str(line[2])+str(line[3])] + [line[col] for col in columns])

if __name__ == '__main__':
    '''
    --------------------------------------------------
    Main program
    --------------------------------------------------
    '''
    # Parse command-line arguments
    prog = os.path.basename(sys.argv[0])
    usage = 'Usage: %s <snp> <cols>\n\n' \
        'Read from standard input; extract rows corresponding to SNP snp;\n' \
        'from each such column, extract the columns cols.\n\n' \
        'Example: cat file | %s exm-IND10-18329639 ''14,15''\n\n' \
        'Type ''%s -h'' to display full help.' % (prog, prog, prog)

    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--separator',
                      default=' ',
                      help='Delimiter [default: %default. Use the string ''\t'' for a tab]')
    parser.add_option('-n', '--headerlines',
                      default=10,
                      help='Number of header lines at the top of the file to skip')
    options, args = parser.parse_args(sys.argv[1:])
    if len(args) < 2:
        print usage
        sys.exit(1)
    snp = args[0]
    columns = [int(col) for col in args[1].split(',')]
    num_header_lines = int(options.headerlines)
    # Support the tab delimiter - must convert it from the string '\t' to the character code \t
    # for the CSV reader to recognize it
    if options.separator == '\\t': options.separator = '\t'
    
    for row in __get_columns(options.separator, snp, columns, num_header_lines):
        print ' '.join(row)
