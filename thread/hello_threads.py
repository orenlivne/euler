#!/usr/bin/env python
#hello_threads.py

import threading
import datetime

class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print "%s says Hello World at time: %s" % (self.getName(), now)

for i in xrange(2):
    t = ThreadClass()
    t.start()
