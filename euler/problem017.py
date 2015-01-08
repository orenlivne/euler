'''
============================================================
http://projecteuler.net/problem=17

If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.

Created on Feb 21, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from problem013 import num_digits

def num2words(x):
    '''Convert x to a list of words. 1 <= x <= 1000, although this should work for larger values.'''
    if x < 10:    # Case 1
        words = [DIGITS[x]]
    elif x < 20:  # Case 2
        words = [TEENS[x]]
    elif x < 100: # Case 2a
        words = [TENS[x / 10]] # Omitting 10* for speed
        y = x % 10
        if y != 0:
            words.append(DIGITS[y])
    else:         # Case 3,4,...
        n = num_digits(x) - 1
        series = 10 ** n
        words = [DIGITS[x / series], SERIES[n]]
        y = x % series
        if y != 0:
            if n == 2:
                words.append('and')
            words += num2words(y) # recursion
    return words

DIGITS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
          6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
TEENS = {10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
         15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
TENS = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty',
        7: 'seventy', 8: 'eighty', 9: 'ninety'}
SERIES = {2: 'hundred', 3: 'thousand'}
    
if __name__ == "__main__":
    #for x in xrange(1, 1001):
    #    print x, ' '.join(num2words(x)), sum(map(len, num2words(x)))
    print sum(sum(map(len, words)) for words in map(num2words, xrange(1, 1001)))    # 21124
    #import doctest
    #doctest.testmod()
