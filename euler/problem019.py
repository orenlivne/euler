'''
============================================================
http://projecteuler.net/problem=19

You are given the following information, but you may prefer to do some research for yourself.

* 1 Jan 1900 was a Monday.
* Thirty days has September,
  April, June and November.
  All the rest have thirty-one,
  Saving February alone,
  Which has twenty-eight, rain or shine.
  And on leap years, twenty-nine.
* A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
sundays = [2, 1, 2, 1, 2, 2, 2] # Sundays per year (starting in March) vs. Mar 1 date. 0=Sunday,...,6=Saturday

def total_sundays(start, stop):
    '''Number of Sundays that fall on the first of the month during the dates
    [1 MAR start, 1 MAR stop).'''
    # Calculate Day of week of 1 MAR start
    mar = (-2 * ((start / 100) % 4) + (start % 100) + ((start % 100) / 4) + 2 + 1) % 7
    count = 0
    for x in xrange(start, stop):
        print x, mar, sundays[mar]
        count += sundays[mar]
        mar += 1
        if is_leap_year(x + 1):
            mar += 1
        mar = mar % 7
    return count

def is_leap_year(x):
    return (x % 4 == 0 and x % 100) or (x % 400 == 0)

if __name__ == "__main__":
    print total_sundays(1901, 2001)
    #import doctest
    #doctest.testmod()
