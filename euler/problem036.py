'''
============================================================
http://projecteuler.net/problem=36

The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)
============================================================
'''
def is_palindrome(x, b):
    '''Is x a palindrome in base b?'''
    digits = []
    while x > 0:
        digits.append(x % b)
        x /= b
    return digits == digits[-1::-1]

def base_digits(x, b):
    '''Return the digits of x in base b, starting with least-significant.'''
    digits = []
    while x > 0:
        digits.append(x % b)
        x /= b
    return digits

def sum_double_palindromes(n, b):
    '''Return the sum of palindromes with < n digits that are also palindromes in base b.'''
    s = 0
    for d in xrange(1, n):
        h, stop = (d + 1) / 2, d % 2
        for x in (x for x in xrange(1, 10 ** h) if x % 10 and x % b):
            x_str = str(x).zfill(h)
            y = int((x_str[-1:0:-1] if stop else x_str[-1::-1]) + x_str)
            if is_palindrome(y, b):
                s += y
    return s

def sum_double_palindromes_brute_force(n, b):
    '''Return the sum of palindromes with < n digits that are also palindromes in base b.'''
    s = 0
    for x in (x for x in xrange(1, 10 ** (n - 1)) if x % 10 and x % b):
        x_str = str(x)
        if x_str == x_str[-1::-1] and is_palindrome(x, b):
            s += x
    return s

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    import time

    # Fast palindrome generation    
    start = time.time()
    print sum_double_palindromes(7, 2)
    print time.time() - start, 'sec'

    # My brute-force
    start = time.time()
    print sum_double_palindromes_brute_force(7, 2)
    print time.time() - start, 'sec'

    # Suzaku's brute-force for b=2, 07 Dec 2012 02:39 am
    start = time.time()
    print(sum(x for x in xrange(1, 1000000, 2) if str(x) == str(x)[::-1] and bin(x)[2:] == bin(x)[:1:-1]))
    print time.time() - start, 'sec'
    