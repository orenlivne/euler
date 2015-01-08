'''
============================================================
Testing shared memory objects in multiprocessing.
TODO: convert to a test case

Created on June 17, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import numpy as np, time
from multiprocessing import Pool, Manager

class MyNum(object):
    def __init__(self, x):
        print 'MyNum(%d)' % (x,)
        self.x = x
        
def f(x):
    time.sleep(3)  # np.random.randint(3))
    return x.x * x.x

if __name__ == '__main__':
    manager = Manager()
    lock = manager.Lock()
    pool = Pool(processes=1)  # start 4 worker processes
    result = [None] * 10
    for i, x in enumerate(xrange(5, 15)):
        result[i] = pool.apply_async(f, [MyNum(x)])  # evaluate "f(10)" asynchronously
        print 'after apply, x %d' % (x,)
    t = time.time()
    for i in xrange(10):
        print result[i].get(timeout=10)  # prints "100" unless your computer is *very* slow
    print 'Total time %.2f' % (time.time() - t)
    print pool.map(f, [MyNum(x) for x in xrange(5, 15)])  # prints "[0, 1, 4,..., 81]"
    
