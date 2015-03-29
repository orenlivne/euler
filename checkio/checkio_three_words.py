'''
============================================================
You are given a string with words and numbers separated by whitespaces (one space). The words contains only letters. You should check if the string contains three words in succession. For example, the string "start 5 one two three 7 end" contains three words in succession.

Input: A string with words.

Output: The answer as a boolean.

http://www.checkio.org/mission/three-words/

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import re

def has_n_consecutive_words(words, n):
    word_pattern = re.compile('^[a-zA-Z]+$')
    num_consecutive_words = 0
    for token in words.split():
        num_consecutive_words = (num_consecutive_words+1) if word_pattern.match(token) else 0
        if num_consecutive_words == n: return True
    return False
        
def checkio(words):
    return has_n_consecutive_words(words, 3)

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(u"Hello World hello") == True, "Hello"
    assert checkio(u"He is 123 man") == False, "123 man"
    assert checkio(u"1 2 3 4") == False, "Digits"
    assert checkio(u"bla bla bla bla") == True, "Bla Bla"
    assert checkio(u"Hi") == False, "Hi"
