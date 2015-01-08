'''
============================================================
Testing shared memory objects in multiprocessing.
TODO: convert to a test case

Created on June 17, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from multiprocessing import Pool, TimeoutError
import time

def f(x): return x * x

class MyObject(object):
    def f(self, x): return x * x

def g((a, x)): return a.f(x) 

if __name__ == '__main__':
    pool = Pool(processes=4)  # start 4 worker processes

    result = pool.apply_async(f, (10,))  # evaluate "f(10)" asynchronously
    print result.get(timeout=1)  # prints "100" unless your computer is *very* slow

    print pool.map(f, xrange(10))  # prints "[0, 1, 4,..., 81]"

    it = pool.imap(f, xrange(10))
    print it.next()  # prints "0"
    print it.next()  # prints "1"
    print it.next(timeout=1)  # prints "4" unless your computer is *very* slow

    result = pool.apply_async(time.sleep, (10,))
    try:
        print result.get(timeout=1)  # raises TimeoutError
        raise ValueError('We shouldn''t be here')
    except TimeoutError: pass

    a = MyObject()        
    #print pool.map(a.f, xrange(10))  # raises PicklingError
    print pool.map(g, ((a, x) for x in xrange(10)))  # prints "[0, 1, 4,..., 81]"
