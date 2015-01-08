'''
============================================================
http://projecteuler.net/problem=98

By replacing each of the letters in the word CARE with 1, 2, 9, and 6 respectively, we form a square number: 1296 = 362. What is remarkable is that, by using the same digital substitutions, the anagram, RACE, also forms a square number: 9216 = 962. We shall call CARE (and RACE) a square anagram word pair and specify further that leading zeroes are not permitted, neither may a different letter have the same digital value as another letter.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, find all the square anagram word pairs (a palindromic word is NOT considered to be an anagram of itself).

What is the largest square number formed by any member of such a pair?

NOTE: All anagrams formed must be contained in the given text file.
============================================================
'''
import itertools as it

all_different = lambda x: all(x[i] != x[i + 1] for i in xrange(len(x) - 1))
groupby_sorted = lambda lst: ((k, list(v for _, v in g)) for k, g in it.groupby(sorted((''.join(sorted(x)), x) for x in lst), lambda pair: pair[0]))
read_words = lambda file_name: (x[1:-1] for x in open(file_name, 'rb').next().rstrip('\r\n').rstrip('\n').split(','))
digitize = lambda d, x: ''.join(it.imap(d.get, x))
anagrams = lambda words: sorted((v for _, v in groupby_sorted(words) if len(v) > 1), key=lambda s: len(s[0]), reverse=True)
squares = lambda n: dict((k, v) for k, v in groupby_sorted(map(str, (x * x for x in xrange(int((10 ** (n - 1)) ** 0.5), int((10 ** n - 1) ** 0.5) + 1)))) if len(v) > 1 and all_different(k))
MAX_SIZE = 1000

def max_square_anagram(words):
    '''Returns the largest square number formed by any member of a square anagram word pair
    in the word list ''words'', or 0, if no such pair is found.'''
    max_square, sz, alphabet_sz, a = 0, MAX_SIZE, MAX_SIZE, anagrams(words)
    for b in a:  # a is ordered in decreasing word size
        alphabet = set(b[0])  # Set of distinct letters in each of the words in the bin 'bin'
        current_sz, current_alphabet_sz = len(b[0]), len(alphabet)
        if current_sz < sz:  # Smaller word size reached, initialize new permissible squares dictionary
            if max_square: return max_square  # If any anagram square pair was found in the previous size, return it since we will not find any bigger ones at smaller sizes
            sz = current_sz
        if current_alphabet_sz != alphabet_sz:
            alphabet_sz = current_alphabet_sz
            s = squares(current_sz)
        for x, y in it.combinations(b, 2):
            for k, v in s.iteritems():
                for pk in (''.join(pk) for pk in it.permutations(k)):
                    d = dict(zip(alphabet, pk))  # Digital assignment of letters
                    X, Y = digitize(d, x), digitize(d, y)
                    if X in v and Y in v:
                        max_square = max(max_square, int(X), int(Y))
    return max_square  # max attained at the minimum word size or no anagram square pairs found  
        
if __name__ == "__main__":
    import time
    start = time.time()
    print max_square_anagram(read_words('problem098.dat'))
    print time.time() - start, 'sec'
