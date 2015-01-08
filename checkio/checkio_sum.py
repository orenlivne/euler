'''
============================================================
http://checkio.org

return the sum of a list of integers w/out using the
following words:

sum, import, for, while, reduce.
============================================================
'''
def mysum(a):
    '''Sum the list a.''' 
    return (a[0] + mysum(a[1:])) if a else 0

#---------------------------------------------
# Testing
#---------------------------------------------
from numpy.ma.testutils import assert_equal

def test_case_sum(impl, a):
    assert_equal(impl(a), sum(a))

def test_sum(impl):
    for s in ([], [1], [1, 2], [1, 2, 3]):
        test_case_sum(impl, s)

if __name__ == "__main__":
    test_sum(mysum)
  
