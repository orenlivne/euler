#!/usr/bin/env python
import sys, os
from optparse import OptionParser

if __name__ == '__main__':
    PROGRAM = os.path.basename(sys.argv[0])
    usage = 'Usage: %s <config_file> [config_args]\n\n' \
            'Generate a condor fan DAG pipeline. The config arguments are passed to\n' \
            'the placeholders arg0...arg{N-1} in the config file.\n\n' \
            'Example: %s example.fan input.txt will add %%(arg0)s = input.txt to\n' \
            'configuration read from example.fan.\n\n' \
            'Type ''%s -h'' to display full help.' % (PROGRAM, PROGRAM, PROGRAM)
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--debug'        , action='store_true', dest='debug', default=False,
                      help='Print debugging information')
    parser.add_option('-s', '--start-chr'          , type='int', dest='start_chr', default=1,
                      help='Start Chromosome number')
    print 'CLI argv', sys.argv
    (options, args) = parser.parse_args(sys.argv[1:])
    print 'args', args
    print 'options', options
    
