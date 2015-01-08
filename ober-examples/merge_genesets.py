#!/usr/bin/env python
'''
============================================================
Merge gene data files. The intersection of
(chromosome,location) pairs in all files is found, and the
lines in all files are concatenated and output for each
common pair. 

Example: 
merge_genesets.py -s ' ' -c 0,1 tests/geneset1.txt tests/geneset2.txt tests/geneset3.txt

will use the first two columns to intersect the files and output
the concatenation of lines from all files for each intersection
element.    

Created on Jun 20, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys, csv, os
from linecache import getline
from optparse import OptionParser

def _get_columns(filename, separator, columns):
    '''Read the first two columns in a data file.'''
    with file(filename, 'rb') as file_obj:
        # Strip whitespace after delimiter
        for line in csv.reader(file_obj, delimiter=separator, skipinitialspace=True):
            if line:  # Make sure there's at least one entry
                yield tuple([int(line[col]) for col in columns])
                
def hash_file(filename, separator, columns):
    '''Hash file based on the first two columns.'''
    # Could use this instead of _get_columns() if numpy is installed:
    # data = np.genfromtxt(filename, usecols=(0, 1), dtype=long)
    return [line for line in _get_columns(filename, separator, columns)]

def merge_files(*args, **kwargs):
    '''The main call that merges files args into a big file with common hash values.'''
    # For each intersection element of the hash of file lines , return a concatenation of the
    # hash and the corresponding full lines in all files
    separator = kwargs.get('separator', ' ')
    columns = kwargs.get('columns', [0, 1])
    file_hash = (hash_file(filename, separator, columns) for filename in args)
    for row in list_intersection_and_index(*file_hash):
        # Random access to file lines (provided by the python linecache library) is much
        # faster than loading the entire data into memory. 
        # * i is an index into the row (tuple).
        # * linecache is 1-based and row index values are 0-based 
        # * args is 0 based but i is 1-based (row[0] = hash of file line)
        yield separator.join([str(row[0][0]), str(row[0][1])] + 
        [separator.join(getline(args[i - 1], row[i] + 1).rstrip().split()[2:])
         for i in xrange(1, len(row))])

def list_intersection_and_index(*args):
    '''Merge a variable number of lists. Return the intersection and index arrays
    into the intersection.'''
    
    # Compute the intersection of all lists 
    common = frozenset(args[0])
    for i in xrange(1, len(args)): common = common.intersection(frozenset(args[i]))
        
    # Compute membership indices of each element of each list
    index = []
    for a in args:
        index.append(dict((y, x) for (x, y) in enumerate(a) if y in common))
    
    # Return a matrix whose rows contain intersection elements and their index in all lists
    for i in index[0].iterkeys():
        yield [i] + [a[i] for a in index]

if __name__ == '__main__':
    '''
    --------------------------------------------------
    Main program
    --------------------------------------------------
    '''
    # Parse command-line argument
    prog = os.path.basename(sys.argv[0])
    usage = 'Usage: %s [-s separator] [-c col1,...,colN] file1 file2\n\n' \
        'Merge the gene sets in the delimited files file1, file2, ... by\n' \
        'the the specified columns. Merged data is spit into standard output.\n' \
        'Type ''%s -h'' to display full help.' % (prog, prog)

    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--separator',
                      default=' ',
                      help='Delimiter [default: %default]')
    parser.add_option('-c', '--columns',
                      default='0,1',
                      help='Columns to use in comparing file rows [default: %default]')
    (options, filenames) = parser.parse_args(sys.argv[1:])    
    columns = [int(col) for col in options.columns.split(',')]
    if (len(filenames) < 1):
        print usage
        sys.exit(1)
        
    # Merge files
    for line in merge_files(*filenames, columns=columns, separator=options.separator):
        print ' '.join(line)
