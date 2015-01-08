'''
============================================================
http://checkio.org

Check if a string is composed of matching parentheses, e.g.,
( ( ... [ ] { ... } ) ... )
============================================================
'''
OPEN = '([{'
CLOSE = ')]}'
MATCHING = dict(zip(OPEN, CLOSE))

def is_legal_oren(s):
    '''O(n) worst-case time, O(#open parentheses in s) storage where n=len(s).'''
    stack = []
    for c in s:
        if c in OPEN: 
            stack.append(c)
        elif c in CLOSE:
            if stack:
                last = stack.pop()
                if c != MATCHING[last]:
                    return False
            else:
                return False
    return False if stack else True

def is_legal_steve(tooslow):
    '''O(n^2) worst-case time, O(n) storage where n=len(s).'''
    x = filter(lambda x: x.lower() in '(){}[]', tooslow) # No need to use lower()
    h = len(x)
    v = 0
    while h != v:
        h = len(x)
        x = x.replace('()', '')
        x = x.replace('[]', '')
        x = x.replace('{}', '')    
        v = len(x)
    return False if x else True # Was originally return x, which was wrong. Need to return a boolean.

#---------------------------------------------
# Testing
#---------------------------------------------
from numpy.ma.testutils import assert_equal
import time

def test_brackets(impl):
    assert_equal(impl('jfkld;sz()([{}]'), False) 
    assert_equal(impl('(())IIOO[]]['), False) 
    assert_equal(impl('(([dfd{dfdf}]))'), True)
    assert_equal(impl('(((((((((((((((((('), False)

def compare_times():
    n = 100
    for _ in xrange(10):
        s = '(' * n + ')' * n
        start = time.time()
        is_legal_steve(s)
        time1 = time.time() - start
        
        start = time.time()
        is_legal_oren(s)
        time2 = time.time() - start
        print 'n = %6d\tSteve time: %.2f sec\tOren  time: %.2f sec' % (n, time1, time2)
        n *= 2

if __name__ == "__main__":
    test_brackets(is_legal_steve)
    test_brackets(is_legal_oren)
    compare_times()