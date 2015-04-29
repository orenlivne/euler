'''
============================================================
http://www.checkio.org/mission/funny-adding/

Created on Apr 26, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def checkio(data):
    """The sum of two integer elements"""
    return data[0] + data[1]
    
if __name__ == '__main__':
    assert checkio([5, 5]) == 10, 'First'
    assert checkio([7, 1]) == 8, 'Second'
    print('All ok')
