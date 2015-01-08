'''
============================================================
http://projecteuler.net/problem=155

An electric circuit uses exclusively identical capacitors of the same value C. 
The capacitors can be connected in series or in parallel to form sub-units, which can then be connected in series or in parallel with other capacitors or other sub-units to form larger sub-units, and so on up to a final circuit.

Using this simple procedure and up to n identical capacitors, we can make circuits having a range of different total capacitances. For example, using up to n=3 capacitors of 60 F each, we can obtain the following 7 distinct total capacitance values:


If we denote by D(n) the number of distinct total capacitance values we can obtain when using up to n equal-valued capacitors and the simple procedure described above, we have: D(1)=1, D(2)=3, D(3)=7 ...

Find D(18).

Reminder : When connecting capacitors C1, C2 etc in parallel, the total capacitance is CT = C1 + C2 +..., 
whereas when connecting them in series, the overall capacitance is given by: 
============================================================
'''
from itertools import islice, product
from problem005 import gcd

def normalize(x, y):
    '''Reduce the fraction x/y to its normal, irreducible form.'''
    g = gcd(x, y)
    return x / g, y / g

def add_cross_product(d, a, b):
    '''Add all the parallel and sequential combinations of the sets a and b into d.'''
    for (x0, y0), (x1, y1) in product(a, b):
        z = x0 * y1 + x1 * y0
        for combo in ((z, y0 * y1), (x0 * x1, z)): d.add(normalize(combo[0], combo[1]))
    return d

def combo_dict(d_prev):
    '''Return the set d of total capacitance values with n capacitances given d[1],...,d[n-1],
    stored in the list d_prev. d_prev[0] is dummy.'''
    d, n = set(), len(d_prev)
    # n capacitors can be composed of 1+(n-1), 2+(n-2), ..., n/2 + (n-n/2). For each one,
    # calculate the cross product using the previous method and add to the set d[n].
    for i in xrange(1, n / 2 + 1): d = add_cross_product(d, d_prev[i], d_prev[n - i])
    return d
     
def num_cap():
    '''Yield the number of distinct total capacitance values with up to n capacitances, for
      n = 1,2,3,... .'''
    d = [None, set([(1, 1)])]
    d_all = set(d[-1])
    yield len(d_all)
    while True:
        d.append(combo_dict(d))
        d_all |= d[-1]
        yield len(d_all)

if __name__ == "__main__":
    print islice(num_cap(), 17, 18).next()
