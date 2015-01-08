'''
============================================================
http://projecteuler.net/problem=16

2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2^1000?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def power_two_digit_sum(n):
    #return sum(int(x) for x in str(2 ** n))
    # Nicer syntax
    return sum(map(int, str(2 ** n)))

if __name__ == "__main__":
    print power_two_digit_sum(1000) #1366
