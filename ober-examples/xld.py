#!/usr/bin/env python
'''
============================================================
Prune variants so that none is in LD with any variant in
a second list.

Created on January 21, 2014
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys, os
from optparse import OptionParser

def parse_command_line_args(argv):
    '''Parse and validate command-line arguments.'''
    prog = os.path.basename(sys.argv[0])
    usage = 'Usage: %s <list1-file> <list2-file> <ld-file>\n\n' \
        'Prune variants so that none is in LD with any variant in\n' \
        'a second list.\n' \
        '\nType ''%s -h'' to display full help.' % (prog, prog)
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--separator',
                      default=' ',
                      help='Field delimiter in all files [default: %default. Use the string ''\t'' for a tab]')
    options, args = parser.parse_args(sys.argv[1:])
    if len(args) != 3:
        print usage
        sys.exit(1)
    # Support the tab delimiter - must convert it from the string '\t' to the character code \t
    # for the CSV reader to recognize it
    if options.separator == '\\t': options.separator = '\t'
    return args, options

##########################################################################################
'''Main program'''
if __name__ == '__main__':
    args, options = parse_command_line_args(sys.argv)
    
    # Read both lists into python sets -- kept in memory
    snp1 = set(line.strip() for line in open(args[0], 'rb'))
    snp2 = set(line.strip() for line in open(args[1], 'rb'))
        
    # LD file is big; stream and remove elements from snp1 if a record of them
    # being in LD with a snp2 element isfound
    for x1, x2 in (line.strip().split() for line in open(args[2], 'rb')):
        if x1 in snp1 and x2 in snp2: snp1.remove(x1)
        if x1 in snp2 and x2 in snp1: snp1.remove(x2)

    # Remaining elements in snp1 are the pruned set
    for x in snp1: print x
