'''
============================================================
http://projecteuler.net/problem=22

Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938  53 = 49714.

What is the total of all the name scores in the file?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import csv

def read_file(f):
    '''Read name list from input stream.'''
    #return list(x[0][1:-1] for x in csv.reader(f, lineterminator=','))
    return csv.reader(f).next()

def score_sum(s):
    '''Sort name list s and return its total score.'''
    s.sort()
    offset = 1 - ord('A')
    value = lambda x: ord(x) + offset
    return sum((k + 1) * sum(map(value, v)) for k, v in enumerate(s))

if __name__ == "__main__":
    s = read_file(open('problem022.dat', 'rb'))
    print score_sum(s)
#    import doctest
#    doctest.testmod()
