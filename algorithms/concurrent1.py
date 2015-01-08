'''
============================================================
Demo of concurrency using multiprocessing.
============================================================
'''
import sys, time, random
from multiprocessing import Manager, Process, Value, Array

def write(lock, msg):
    if lock: lock.acquire()
    sys.stdout.write(msg)
    sys.stdout.flush()
    if lock: lock.release()

def produce(identifier, buf, lock, num_items):
    write(lock, '[Producer %d] Starting\n' % (identifier,))
    count = 0
    buf.add_producer(identifier)
    while count < num_items:
        item = random.randint(0, 9)
        write(lock, '[Producer %d] About to put %d\n' % (identifier, item))
        buf.put(item)
        write(lock, '[Producer %d] Put %d, fill %d, buffer %s\n' % (identifier, item, buf.fill.value, repr(list(buf.buf))))
        count += 1
        time.sleep(0.5 * random.random())
    buf.remove_producer(identifier)
    
def consume(identifier, buf, lock, num_tries=20):
    write(lock, '[Consumer %d] Starting\n' % (identifier,))
    count = 0
    while buf.is_open(): #and count < num_tries:
        count += 1
        item = buf.get()
        if item: write(lock, '[Consumer %d] Got %d, fill %d, buffer %s\n' % (identifier, item, buf.fill.value, repr(list(buf.buf))))
        time.sleep(0.5 * random.random())
    
class Buffer(object):
    def __init__(self, capacity, lock):
        self.capacity, self.lock, self.fill, self.num_producers, self.buf, self.open = \
        capacity, lock, Value('i', 0), Value('i', 0), Array('i', [-1] * capacity), Value('i', 1)
    
    def is_open(self):
        return self.open.value

    def add_producer(self, identifier):
        self.lock.acquire()
        self.num_producers.value += 1
        write(None, '[Buffer] Registering %d\n' % (identifier,))
        self.lock.release()
    
    def remove_producer(self, identifier):
        self.lock.acquire()
        if self.num_producers.value == 0: raise ValueError('Bad ref count')
        self.num_producers.value -= 1
        write(None, '[Buffer] Removing %d\n' % (identifier,))
        if self.num_producers.value == 0:
            self.open.value = 0
            write(None, '[Buffer] Closing\n')
        self.lock.release()
        
    def put(self, item):
        self.lock.acquire()
        if self.fill.value < self.capacity:
            self.buf[self.fill.value] = item
            self.fill.value += 1
        self.lock.release() 
        
    def get(self):
        self.lock.acquire()
        item = None
        if self.fill.value > 0:
            item = self.buf[self.fill.value - 1]
            self.fill.value -= 1
        self.lock.release()
        return item
        
    def open(self):
        self.lock.acquire()
        op = (self.num_producers.value > 0)
        self.lock.release()
        return op
    
if __name__ == "__main__":
    m = Manager()
    lock = m.Lock()
    buf = Buffer(8, lock)
    c = [Process(target=consume, args=(i, buf, lock)) for i in xrange(3)]
    for x in c: x.start()
    p = [Process(target=produce, args=(i, buf, lock, 10)) for i in xrange(3)]
    for x in p: x.start()

    for x in p: x.join()
    for x in p: x.join()
