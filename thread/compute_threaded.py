#!/usr/bin/env python
'''Sum up the first 100000000 numbers. Time the speed-up of using multithreading.'''
import threading, time, numpy as np

class SumThread(threading.Thread):
    def __init__(self, a, b):
        threading.Thread.__init__(self)
        self.a = a
        self.b = b
        self.s = 0

    def run(self):
        self.s = sum(i for i in xrange(self.a, self.b))

def main(num_threads):
    start = time.time()
    a = map(int, np.core.function_base.linspace(0, 100000000, num_threads + 1, True))
    # spawn a pool of threads, and pass them queue instance
    threads = []
    for i in xrange(num_threads):
        t = SumThread(a[i], a[i + 1])
        t.setDaemon(True)
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Fetch results
    s = sum(t.s for t in threads)
    print '#threads = %d, result = %10d, elapsed Time: %s' % (num_threads, s, time.time() - start)
    
for n in 2 ** np.arange(4):
    main(n)
