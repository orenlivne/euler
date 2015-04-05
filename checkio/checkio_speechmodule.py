'''
============================================================
http://www.checkio.org/mission/speechmodule/solve/

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
FIRST_TEN = ["one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
SECOND_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
OTHER_TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
              "eighty", "ninety"]
HUNDRED = "hundred"


def checkio(number):
    words = []
    
    hundreds = number / 100
    if hundreds > 0:
        words.append(FIRST_TEN[hundreds-1])
        words.append(HUNDRED)
    
    number = number % 100
    tens = number / 10
    if tens == 1:
        number = number % 10
        words.append(SECOND_TEN[number])
        return ' '.join(words)
    elif tens > 0: words.append(OTHER_TENS[tens-2])

    number = number % 10
    if number > 0: words.append(FIRST_TEN[number-1])
    return ' '.join(words)

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(4) == 'four', "1st example"
    assert checkio(133) == 'one hundred thirty three', "2nd example"
    assert checkio(12) == 'twelve', "3rd example"
    assert checkio(101) == 'one hundred one', "4th example"
    assert checkio(212) == 'two hundred twelve', "5th example"
    assert checkio(40) == 'forty', "6th example"
    assert not checkio(212).endswith(' '), "Don't forget strip whitespaces at the end of string"
