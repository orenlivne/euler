'''
============================================================
http://projecteuler.net/problem=186

Here are the records from a busy telephone system with one million users:

RecNr    Caller    Called
1    200007    100053
2    600183    500439
3    600863    701497
...    ...    ...
The telephone number of the caller and the called number in record n are Caller(n) = S2n-1 and Called(n) = S2n where S1,2,3,... come from the "Lagged Fibonacci Generator":

For 1 <= k <= 55, Sk = [100003 - 200003k + 300007 k**3] (modulo 1000000)
For 56 <= k, Sk = [Sk-24 + Sk-55] (modulo 1000000)

If Caller(n) = Called(n) then the user is assumed to have misdialled and the call fails; otherwise the call is successful.

From the start of the records, we say that any pair of users X and Y are friends if X calls Y or vice-versa. Similarly, X is a friend of a friend of Z if X is a friend of Y and Y is a friend of Z; and so on for longer chains.

The Prime Minister's phone number is 524287. After how many successful calls, not counting misdials, will 99% of the users (including the PM) be a friend, or a friend of a friend etc., of the Prime Minister?
============================================================
'''
N = 10 ** 6

def lag():
    '''Lagged Fibonacci Generator.'''
    s = [(100003 - (200003 - 300007 * k * k) * k) % N for k in xrange(1, 56)]
    for x in s: yield x
    while True:
        x = (s[-55] + s[-24]) % N
        yield x
        for i in xrange(54): s[i] = s[i + 1]
        s[-1] = x

def edges():
    '''A generator of successful telephone (caller, called) pairs.'''
    s = lag()
    while True:
        x, y = s.next(), s.next()
        if x != y: yield x, y
    
cid = lambda c: c[0]
    
def min_edges_for_large_comp(node_iter, edge_iter, proband, threshold):
    '''Return the minimum number of edges required to be added to the network for the connected
    component containing the node ''proband'' to have at least ''threshold'' nodes, or -1, if
    this never happens.'''
    if 1 >= threshold: return 0
    c = [[x] for x in node_iter]  # c[x] = connected component of node x
    for m, (x, y) in enumerate(edge_iter, 1):
        cx, cy = c[x], c[y]
        # Reorder edge so that cx is the larger component to reduce the number of c[z] assignments
        # below, where z is connected to y
        if len(cx) < len(cy): x, y, cx, cy = y, x, cy, cx
        cid_x = cid(cx)
        if cid_x != cid(cy):  # y and x not connected yet, merge their components
            for z in cy: cx.append(z)
            for z in cy: c[z] = cx
            # Only need to check the proband's component size if it changed by the recent merge
            if cid_x == cid(c[proband]) and len(c[proband]) >= threshold: return m
    return -1  # Component never exceeds threshold
    
if __name__ == "__main__":
    print min_edges_for_large_comp(xrange(N), edges(), 524287, .99 * N)
