#!/usr/bin/env python
#------------------------------------------------------
# Example program for Martin Depner.
# Read lines from a text file. Count how many times
# the string 'Martin' appears in the file.
#
# See read_lines.pl for the Perl counterpart.
#------------------------------------------------------

file_name = 'perl/martin.in'
s = 'Martin'

count = 0
with open(file_name,'r') as my_input_file:
    for line in my_input_file:
        line = line.rstrip()
        if (line == s):
            count = count+1

print 'Number of times', s, 'appears', count
