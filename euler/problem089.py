'''
============================================================
http://projecteuler.net/problem=89

The rules for writing Roman numerals allow for many ways of writing each number (see About Roman Numerals...). However, there is always a "best" way of writing a particular number.

For example, the following represent all of the legitimate ways of writing the number sixteen:

IIIIIIIIIIIIIIII
VIIIIIIIIIII
VVIIIIII
XIIIIII
VVVI
XVI

The last example being considered the most efficient, as it uses the least number of numerals.

The 11K text file, roman.txt (right click and 'Save Link/Target As...'), contains one thousand numbers written in valid, but not necessarily minimal, Roman numerals; that is, they are arranged in descending units and obey the subtractive pair rule (see About Roman Numerals... for the definitive rules for this problem).

Find the number of characters saved by writing each of these in their minimal form.

Note: You can assume that all the Roman numerals in the file contain no more than four consecutive identical units.
============================================================
'''
R2D = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
TO_EXTENDED = {'IV': 'a', 'IX':'b', 'XL':'c', 'XC':'d', 'CD':'e', 'CM':'f'}
R2D_EXTENDED = dict(R2D.items() + [('a', 4), ('b', 9), ('c', 40), ('d', 90), ('e', 400), ('f', 900)])
RVAL = [(k, v, 10 ** ((len(R2D) - i) / 2)) if i % 2 == 0 else v for i, (k, v) in enumerate(sorted(((k, v) for (v, k) in R2D.iteritems()), reverse=True))]

def roman2dec(s):
    for k, v in TO_EXTENDED.iteritems(): s = s.replace(k, v)
    return sum(map(R2D_EXTENDED.get, s))

def dec2roman(x):
    s = ''
    for i, (k, v, b) in enumerate(RVAL[0::2]):
        r, x = divmod(x, b)
        if i == 0: t = ''.join([v] * r)  # MMMM...
        else:
            if r <= 3: t = ''.join([v] * r)  # XXX...
            elif r == 4: t = v + RVAL[2 * i - 1]  # XL...
            elif r <= 8: t = RVAL[2 * i - 1] + ''.join([v] * (r - 5))  # LXXX...
            else: t = v + RVAL[2 * i - 2][1]  # XC...
        s += t
    return s

if __name__ == "__main__":
    for s, x, t, y in [(s, roman2dec(s), dec2roman(roman2dec(s)), roman2dec(dec2roman(roman2dec(s)))) for s in (line.rstrip('\r\n').rstrip('\n') for line in open('problem089.dat', 'rb'))]:
        print '%-20s %-6d %-20s %-6d' % (s, x, t, y)
    print sum(len(s) - len(dec2roman(roman2dec(s))) for s in (line.rstrip('\r\n').rstrip('\n') for line in open('problem089.dat', 'rb')))
