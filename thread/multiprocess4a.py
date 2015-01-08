'''
============================================================
http://stackoverflow.com/questions/4413821/multiprocessing-pool-example

Created on Mar 6, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from multiprocessing import Pool
from time import time
import numpy as np

def CostlyFunction((z, problem, y)):
    r = 0
    a = np.arange(100)
    a = a * y
    for k in problem.x:
        r += z ** (1 / k ** 1.5)
    return r

class Problem(object):
    def __init__(self, x):
        self.x = x
        
if __name__ == "__main__":
    N = 10
    y = np.arange(100)

    currtime = time()
    K = 2000000
    problem = Problem(range(1, K + 2))
    w = sum(map(CostlyFunction, ((i, problem, y) for i in xrange(N))))
    t = time() - currtime
    print 'Serial  : time elapsed: %.2f, result = %f' % (t, w)

    for p in [1, 2, 4]: #[1, 2, 4, 8, 16, 24, 30]:#2 ** np.arange(4):
        currtime = time()
        po = Pool(processes=p)
        res = po.map_async(CostlyFunction, ((i, problem, y) for i in xrange(N)))
        w = sum(res.get())
        tp = time() - currtime
        print '%2d procs: time elapsed: %.2f (%.1fx), result = %f' % (p, tp, t / tp, w)
