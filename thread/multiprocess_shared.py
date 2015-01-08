'''
============================================================
Testing shared memory objects in multiprocessing.
TODO: convert to a test case

Created on June 17, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double

class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]

# class ArrayClass(object):
#     _fields_ = [('x', np.zeros((10,), dtype=np.uint))]

def modify(n, x, s, t, A):
    n.value **= 2
    x.value **= 2
    s.value = s.value.upper()
    for i, x in enumerate(t):
        t[i] = x * x
        
    for a in A:
        a.x **= 2
        a.y **= 2
#     for i, _ in enumerate(B.x):
#         B.x[i] = i

if __name__ == '__main__':
    lock = Lock()

    n = Value('i', 7)
    x = Value(c_double, 1.0 / 3.0, lock=False)
    s = Array('c', 'hello world', lock=lock)
    t = Array('H', [255, 200], lock=lock)
    A = Array(Point, [(1.875, -6.25), (-5.75, 2.0), (2.375, 9.5)], lock=lock)

    p = Process(target=modify, args=(n, x, s, t, A))
    p.start()
    p.join()

    print n.value
    print x.value
    print s.value
    print list(t)
    print [(a.x, a.y) for a in A]
