'''
============================================================
http://www.checkio.org/mission/stair-steps/

Created on Apr 27, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def checkio(numbers):
    return max(*reduce(lambda (s1, s2), x: (s2, max(s1, s2) + x), numbers, (0, 0)))

# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([5, 4, 3, -99, 2, -20]) == 14
    assert checkio([5, -3, -1, 2]) == 6, 'Fifth'
    assert checkio([-11, 69, 77, -51, 23, 67, 35, 27, -25, 95]) == 393, 'Second'
    assert checkio([5, 6, -10, -7, 4]) == 8, 'First'
    assert checkio([-21, -23, -69, -67, 1, 41, 97, 49, 27]) == 125, 'Third'
    print('All ok')
