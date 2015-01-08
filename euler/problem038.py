'''
============================================================
http://projecteuler.net/problem=38

Take the number 192 and multiply it by each of 1, 2, and 3:

192  1 = 192
192  2 = 384
192  3 = 576
By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?
============================================================
'''

def max_pan():
    '''Return the largest 1 to 9 pandigital 9-digit number that can be formed as the
    concatenated product of an integer with (1,2, ... , n) where n > 1.''' 
    y_max = 918273645 # For x=9 ==> lower bound on max
    for x in xrange(9234, 9877):
        y_str = str(x) + str(2 * x)
        if ''.join(sorted(y_str)) == '123456789':
            y = int(y_str)
            if y > y_max:
                y_max = y
    return y_max

def max_pan_brute_force():
    '''Return the largest 1 to 9 pandigital 9-digit number that can be formed as the
    concatenated product of an integer with (1,2, ... , n) where n > 1.''' 
    y_max = 0
    for x in xrange(2, 10000):
        y_str = str(x)
        k = 1
        while len(y_str) < 9:
            k += 1
            y_str += str(k * x)
        if ''.join(sorted(y_str)) == '123456789':
            y = int(y_str)
            if y > y_max:
                y_max = y
    return y_max
    
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    print max_pan()
    print max_pan_brute_force()
