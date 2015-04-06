'''
============================================================
http://www.checkio.org/mission/verify-anagrams

Created on Apr 5, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def standardize(word):
    return sorted(word.lower().replace(' ', ''))

def verify_anagrams(first_word, second_word):
    return standardize(first_word) == standardize(second_word)

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert isinstance(verify_anagrams(u"a", u"z"), bool), "Boolean!"
    assert verify_anagrams(u"Programming", u"Gram Ring Mop") == True, "Gram of code"
    assert verify_anagrams(u"Hello", u"Ole Oh") == False, "Hello! Ole Oh!"
    assert verify_anagrams(u"Kyoto", u"Tokyo") == True, "The global warming crisis of 3002"
