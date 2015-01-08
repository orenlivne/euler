#!/usr/bin/env python
'''
============================================================
Prune variants for LD. In each LD block, keep the variant
with the highest call rate.

Created on January 21, 2014
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys, os, linecache, networkx as nx, numpy as np
from optparse import OptionParser
from numpy.lib.function_base import corrcoef

def parse_command_line_args(argv):
    '''Parse and validate command-line arguments.'''
    prog = os.path.basename(sys.argv[0])
    usage = 'Usage: %s <map-file> <genotype-file>\n\n' \
        'Prune variants for LD. In each LD block, keep the variant\n' \
        'with the highest call rate.\n' \
        'Input:\n' \
        'map-file: a file with a list of SNP names and call rates.\n' \
        'genotype-file: a file with genotypes in dosage format. One row per SNP. Matches map-file ordering. Missing genotypes should be encoded as -1, dosages as 0,1,2.\n\n' \
        'Output:\n' \
        'list of SNP IDs. Pruned with the specified r^2 threshold.\n' \
        'LD graph, saved in NPZ format to map-file.graph.npz.\n' \
        '\nType ''%s -h'' to display full help.' % (prog, prog)
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--separator',
                      default=' ',
                      help='Genotype-file delimiter [default: %default. Use the string ''\t'' for a tab]')
    parser.add_option('-r', '--r2-threshold' , type='float', dest='r2_min', default=0.3,
                      help='rsq threshold, continue calculating rsq until rsq is less than this value')
    parser.add_option('-p', '--pruning-threshold' , type='float', dest='r2_prune', default=0.99,
                      help='SNPs are partitioned into blocks such that rsq < this threshold for SNPs in different blocks.')
    parser.add_option('-v', '--debug'        , action='store_true'  , dest='debug', default=False,
                      help='Print debugging information')
    parser.add_option('-w', '--min-window-size' , type='int', dest='min_window_size', default=20,
                      help='At least these many neighbors of every will be considered in rsq calculations')
    parser.add_option('-a', '--append-edges-file' , type='str', dest='edges_file', default=None,
                      help='If true, loads graph from map-file.graph; adds edges from the edges_file file, and re-calculates new pruned SNPs')
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
        '''Initialize a genotype loader from the file \'file_name\'.'''
        self.file_name = file_name

    def __getitem__(self, i):
        '''Load genotype line i from the file f.'''
        return GenotypeLoader.__parse_genotypes(linecache.getline(self.file_name, i + 1))

    @staticmethod  
    def __parse_genotypes(line):
        '''Parse a genotype line into a vector of genotype dosages.'''
        return np.array(map(float, line.split()))
    
def r2(x, y):
    '''Calculate the Pearson correlation coefficient between the vectors x and y.'''
    has_data = (x >= 0) & (y >= 0)
    return corrcoef(x[has_data], y[has_data])[0][1] ** 2

def r2_edgelist(file_name, n, r2_min, min_window_size, snp, debug=False):    
    '''Yield the list of tuples (i,j,r^2(i,j)) in the file file_name, where i,j are line numbers.
    Stop calculating r^2 around a SNP when it goes below the threshold r2_min.'''
    g = GenotypeLoader(file_name)
    for i in xrange(n):
        Gi, j_min = g[i], i + min_window_size
        # if debug: print i, snp[i]
        for j in xrange(i, n):
            rsq = r2(Gi, g[j])
            # if debug: print '\t', j, snp[j], rsq
            if rsq < r2_min and j >= j_min: break  # If outside minimum window and small r^2, break
            yield i, j, rsq
        if debug:
            if i % 100 == 0: sys.stderr.write('i=%d (%s), %d neighbors\n' % (i, snp[i], j - i))

def best_in_block(block, priority):
    '''Return the (a) best SNP (attains the highest priority) in a list block of SNPs.''' 
    return max((priority[snp], snp) for snp in block)[1]

'''Main program'''
if __name__ == '__main__':
    args, options = parse_command_line_args(sys.argv)
    graph_file = args[0] + '.graph.npz'
    
    # Read SNP list into arrays; SNPs and priorities into a dictionary
    snp = [line.rstrip().split()[0] for line in open(args[0], 'rb')]
    priority = dict((x[0], float(x[1])) for x in (line.rstrip().split() for line in open(args[0], 'rb')))
    if options.debug: sys.stderr.write('Original #SNPs = %d\n' % (len(snp),))
    if options.edges_file:
        # Load existing graph from file, add custom edges from options.edges_file, reprune
        G = np.load(graph_file)['G'][0]
        if options.debug: sys.stderr.write('Loaded graph from %s, #edges = %d\n' % (graph_file, G.number_of_edges(),))
        G.add_edges_from((x[0], x[1]) for x in (x.rstrip().split() for x in open(options.edges_file, 'rb')))
        if options.debug: sys.stderr.write('After adding custom edges, #edges = %d\n' % (G.number_of_edges(),))
    else:
        if options.debug: sys.stderr.write('Creating LD graph\n')
        # Calculate r^2 and generate graph for the first time
        G = nx.from_edgelist((snp[i], snp[j]) for i, j, rsq in r2_edgelist(args[1], len(snp), options.r2_min, options.min_window_size, snp, debug=options.debug) if rsq >= options.r2_prune)
    # Prune for LD, print best SNP in every LD block, save graph to file
    if options.debug: sys.stderr.write('Saving LD graph to %s\n' % (graph_file,))
    np.savez(graph_file, G=np.array([G]))
    for block in nx.connected_components(G):
        print best_in_block(block, priority)
