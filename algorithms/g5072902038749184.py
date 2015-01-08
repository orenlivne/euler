'''
============================================================
You visited a list of places recently, but you do not remember the 
order in which you visited them. You have with you the airplane 
tickets that you used for travelling. Each ticket contains just the 
start location and the end location. Can you reconstruct your journey?
============================================================
'''
def journey(edges):
    # Find the beginning point
    ends = set(e[1] for e in edges)
    for s in (e[0] for e in edges):
        if not s in ends: break
        d = dict(edges)
    yield s
    for _ in xrange(len(ends)):
        s = d[s]
        yield s

if __name__ == "__main__":
    import numpy as np
    from numpy.ma.testutils import assert_equal
    edges = [(i, i + 1) for i in xrange(10)]
    np.random.shuffle(edges)
    print edges
    print list(journey(edges))
    assert_equal(list(journey(edges)), range(11), 'Wrong reconstructed journey')
