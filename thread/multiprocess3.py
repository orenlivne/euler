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

def f(l, i):
    l.acquire()
    sys.stdout.write('hello world %d\n' % (i,))
    l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in xrange(10):
        Process(target=f, args=(lock, num)).start()
