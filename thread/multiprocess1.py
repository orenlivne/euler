'''
============================================================
Faster than threading? Examples from
http://docs.python.org/2/library/multiprocessing.html

Created on Mar 6, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from multiprocessing import Process
import os

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def f(name):
    info('function f')
    print 'hello', name

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
