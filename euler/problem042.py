'''
============================================================
http://projecteuler.net/problem=42

The nth term of the sequence of triangle numbers is given by, tn = 0.5 n(n+1); so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?
============================================================
'''
import csv, math

OFFSET = ord('A') - 1

def is_triangle(t):
    '''Is t a triangle number?'''
    n = 0.5 * (-1 + math.sqrt(1 + 8 * t))
    return n - math.floor(n) < 1e-15

is_triangle_word = lambda w : is_triangle(sum(ord(x) - OFFSET for x in w))
num_triangle_words = lambda f: sum(1 for w in f if is_triangle_word(w))
read_words_csv = lambda f: (w for w in csv.reader(open(f, 'rb'), lineterminator=',').next())
read_words = lambda f: (w[1:-1] for w in read_file(open(f, 'rb'), delimiter=','))

def read_file(f, delimiter='\n'):
    buf = ''
    while True:
        x = f.read(1)
        if x:
            if x == delimiter:
                yield buf
                buf = ''
            else:
                buf += x
        else:        
            break
        
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    #print [w for w in list(csv.reader(open('problem042.dat', 'rb'), lineterminator=','))[0]]
    #print list(read_words('problem042.dat'))
    print num_triangle_words(read_words('problem042.dat'))
    
