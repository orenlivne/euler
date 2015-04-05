from collections import Counter

LETTERS = set([chr(x) for x in xrange(ord('a'), ord('z')+1)])

def checkio(text):
    c =Counter(x for x in text.lower()if x in LETTERS)
    max_freq = max(c.itervalues())
    return min(x for x,freq inc.iteritems() if freq == max_freq)

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(u"Hello World!") == "l", "Hello test"
    assert checkio(u"How do you do?") == "o", "O is most wanted"
    assert checkio(u"One") == "e", "All letter only once."
    assert checkio(u"Oops!") == "o", "Don't forget about lower case."
    assert checkio(u"AAaooo!!!!") == "a", "Only letters."
    assert checkio(u"abe") == "a", "The First."
    print("Start the long test")
    assert checkio(u"a" * 9000 + u"b" * 1000) == "a", "Long."
    print("The local tests are done.")
