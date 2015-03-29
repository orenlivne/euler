'''
============================================================
Do you remember the radix and Numeral systems from math class? Let's practice with it.
You are given a positive number as a string along with the radix for it. Your function should convert it into decimal form. The radix is less than 37 and greater than 1. The task uses digits and the letters A-Z for the strings.
Watch out for cases when the number cannot be converted. For example: "1A" cannot be converted with radix 9. For these cases your function should return -1.
Input: Two arguments. A number as string and a radix as an integer.
Output: The converted number as an integer.
Precondition: 
re.match("\A[A-Z0-9]\Z", str_number)
0 < len(str_number) <= 10
2 <= radix <= 36

http://www.checkio.org/mission/number-radix

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
LETTERS = [chr(x) for x in xrange(ord('a'), ord('z') + 1)]

def digits_to_number(digits, radix):
    '''Returns the number x corresponding to the digits of x in base radix. digits starts with 
    the most-significant digit.'''
    # Horner's rule.
    x = 0
    for digit in digits: x = radix * x + digit
    return x

def checkio(str_number, radix):
    if radix > len(LETTERS) + 10: raise ValueError('Radix too large for our alphabet')
    if radix < 1: raise ValueError('Radix must be at least 1')
    char_to_digits = dict(zip(map(str, xrange(min(radix, 10))), xrange(min(radix, 10))))
    if radix > 10: char_to_digits.update(dict(zip(LETTERS[:radix - 10], xrange(10, radix))))
    try: return digits_to_number(map(char_to_digits.__getitem__, str_number.lower()), radix)
    except KeyError: return -1

# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(u"AF", 16) == 175, "Hex"
    assert checkio(u"101", 2) == 5, "Bin"
    assert checkio(u"101", 5) == 26, "5 base"
    assert checkio(u"Z", 36) == 35, "Z base"
    assert checkio(u"AB", 10) == -1, "B > A > 10"
