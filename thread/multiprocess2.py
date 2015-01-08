'''
============================================================
Faster than threading? Examples from
http://docs.python.org/2/library/multiprocessing.html

Created on Mar 6, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import sys
from multiprocessing import Process, Lock

def f(l, i, problem):
    l.acquire()
    sys.stdout.write('hello world %d - problem.x = %d\n' % (i, problem.x))
    l.release()

class Problem(object):
    def __init__(self, x):
        self.x = x

if __name__ == '__main__':
    lock = Lock()
    problem = Problem(20)
    for num in xrange(10):
        Process(target=f, args=(lock, num, problem)).start()
