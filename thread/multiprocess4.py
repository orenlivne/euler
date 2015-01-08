'''
============================================================
http://stackoverflow.com/questions/4413821/multiprocessing-pool-example

Created on Mar 6, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from multiprocessing import Pool
from time import time
#import numpy as np

K = 200000
def CostlyFunction((z,)):
    print (z,)
    r = 0
    for k in xrange(1, K + 2):
        r += z ** (1 / k ** 1.5)
    return r

if __name__ == "__main__":
    currtime = time()
    N = 10
    w = sum(map(CostlyFunction, ((i,) for i in xrange(N))))
    t = t = time() - currtime
    print 'Serial  : time elapsed: %.2f, result = %f' % (t, w)

    for p in [1, 2, 4, 8, 16, 24, 30]:#2 ** np.arange(4):
        currtime = time()
        po = Pool(processes=p)
        res = po.map_async(CostlyFunction, ((i,) for i in xrange(N)))
        w = sum(res.get())
        tp = time() - currtime
        print '%2d procs: time elapsed: %.2f (%.1fx), result = %f' % (p, tp, t / tp, w)
