'''
============================================================
http://projecteuler.net/problem=99

Comparing two numbers written in index form like 211 and 37 is not difficult, as any calculator would confirm that 211 = 2048  37 = 2187.

However, confirming that 632382518061  519432525806 would be much more difficult, as both numbers contain over three million digits.

Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K text file containing one thousand lines with a base/exponent pair on each line, determine which line number has the greatest numerical value.

NOTE: The first two lines in the file represent the numbers in the example given above.
============================================================
'''
from math import log

if __name__ == "__main__":
    print max((v, k) for k, v in enumerate(map(lambda (x, y): log(x) * y, (map(int, x.rstrip('\r\n').rstrip('\n').split(',')) for x in open('problem099.dat', 'rb'))), 1))[1]
