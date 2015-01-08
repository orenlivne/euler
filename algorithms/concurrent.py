'''
============================================================
Demo of concurrency using multiprocessing.
============================================================
'''
import sys, time, random
from multiprocessing import Manager, Process

def produce(identifier, buf, lock, num_items):
    lock.acquire()
    sys.stdout.write('[Producer %d] Starting\n' % (identifier,))
    lock.release()
    count = 0
    buf.add_producer(identifier)
    while count < num_items:
        item = random.randint(0, 9)
        lock.acquire()
        sys.stdout.write('[Producer %d] About to put %d\n' % (identifier, item))
        lock.release()
        buf.put(item)
        lock.acquire()
        sys.stdout.write('[Producer %d] Put %d, fill %d\n' % (identifier, item, buf.fill))
        lock.release()
        count += 1
        time.sleep(0.5 * random.random())
    buf.remove_producer(identifier)
    
def consume(identifier, buf, lock):
    lock.acquire()
    sys.stdout.write('[Consumer %d] Starting\n' % (identifier,))
    lock.release()
    while True:
        if not buf.is_open(): break
        lock.acquire()
        sys.stdout.write('[Consumer %d] About to get is_open? %s\n' % (identifier, buf.is_open()))
        lock.release()
        item = buf.get()
        lock.acquire()
        if item: sys.stdout.write('[Consumer %d] Got %d, fill %d\n' % (identifier, item, buf.fill))
        lock.release()
        time.sleep(2 * random.random())
    
class Buffer(object):
    def __init__(self, capacity, lock):
        self.capacity, self.lock, self.fill, self.num_producers, self.buf, self.open = \
        capacity, lock, 0, 0, [None] * capacity, True
    
    def is_open(self):
        self.lock.acquire()
        op = self.open
        self.lock.release()
        return op 

    def add_producer(self, identifier):
        self.lock.acquire()
        self.num_producers += 1
        sys.stdout.write('[Buffer] Registering %d\n' % (identifier,))
        self.lock.release() 
    
    def remove_producer(self, identifier):
        self.lock.acquire()
        if self.num_producers == 0: raise ValueError('Bad ref count')
        self.num_producers -= 1
        sys.stdout.write('[Buffer] Removing %d\n' % (identifier,))
        if self.num_producers == 0:
            self.open = False
            sys.stdout.write('[Buffer] Closing\n')
        self.lock.release()
        
    def put(self, item):
        self.lock.acquire()
        if self.fill < self.capacity:
            self.buf.append(item)
            self.fill += 1
        self.lock.release() 
        
    def get(self):
        self.lock.acquire()
        item = None
        if self.fill > 0:
            item = self.buf.pop()
            self.fill -= 1
        self.lock.release()
        return item
        
    def open(self):
        self.lock.acquire()
        op = (self.num_producers > 0)
        self.lock.release()
        return op
        
if __name__ == "__main__":
    m = Manager()
    lock = m.Lock()
    buf = Buffer(8, lock)
    p = [Process(target=produce, args=(i, buf, lock, 10)) for i in xrange(1)]
    c = [Process(target=consume, args=(i, buf, lock)) for i in xrange(1)]
    for x in c:
        x.start()
    for x in p:
        x.start()
    for x in p:
        x.join()
    for x in c:
        x.join()
