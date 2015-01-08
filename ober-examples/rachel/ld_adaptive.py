#!/usr/bin/env python
'''
============================================================
Calculate the pairwise LD r^2 among a list of SNPs. Only
SNPs that are within a window-length from each other are
included.

Created on January 15, 2014
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys, os, linecache
from optparse import OptionParser
from numpy.lib.function_base import corrcoef

def parse_command_line_args(argv):
    '''Parse and validate command-line arguments.'''
    prog = os.path.basename(sys.argv[0])
    usage = 'Usage: %s <map-file> <genotype-file>\n\n' \
        'Calculate the pairwise LD r^2 among a list of SNPs. Only SNPs\n' \
        'that are within a window-length from each other are included.\n' \
        'Input:\n' \
        'map-file: a file with a list of SNP names\n' \
        'genotype-file: a file with genotypes in dosage format. One row per SNP. Matches map-file ordering.\n\n' \
        'Output:\n' \
        'SNP1 SNP2 r^2 for all pairs within the window length.\n' \
        '\nType ''%s -h'' to display full help.' % (prog, prog)
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--separator',
                      default=' ',
                      help='Genotype-file delimiter [default: %default. Use the string ''\t'' for a tab]')
    parser.add_option('-t', '--threshold' , type='float', dest='t', default=0.3,
                      help='rsq threshold, continue calculating rsq until rsq is less than this value')
    options, args = parser.parse_args(sys.argv[1:])
    if len(args) != 2:
        print usage
        sys.exit(1)
    # Support the tab delimiter - must convert it from the string '\t' to the character code \t
    # for the CSV reader to recognize it
    if options.separator == '\\t': options.separator = '\t'
    return args, options

class GenotypeLoader(object):
    '''Loads genotypes from a genotype file.'''
    
    def __init__(self, file_name):
        self.file_name = file_name
#        print file_name

    '''Parse a genotype line into a vector of genotype dosages.'''
    @staticmethod  
    def __parse_genotypes(line):
#        print line
        return map(float, line.split())
    
    def __getitem__(self, i):
        '''Load genotype line i from the file f.'''
        return GenotypeLoader.__parse_genotypes(linecache.getline(self.file_name, i + 1))

def r2(x, y):
    '''Calculate the Pearson correlation coefficient between the vectors x and y.'''
#    print x, y
#    print corrcoef(x, y)
    return corrcoef(x, y)[0][1] ** 2

if __name__ == '__main__':
    '''
    --------------------------------------------------
    Main program
    --------------------------------------------------
    '''
    args, options = parse_command_line_args(sys.argv)
    
    # Read SNP list into the snps array
    snps = [line.rstrip() for line in open(args[0], 'rb')]
    n = len(snps)
    
    # Loop over SNPs; for each one, loop over forward neighbors
    g = GenotypeLoader(args[1])
    for i in xrange(n):
        Gi = g[i]
        r = 1.00
        j = i
        while(r > options.t and j < n):
        # for j in xrange(i, min(i + options.window_size, n)):
            Gj = g[j]
            # For each (SNP, neighbor SNP) pair, calculate R^2 and print
            r = r2(Gi, Gj)
            print snps[i], snps[j], r
            j += 1
