'''
============================================================
Let's continue examining words. You are given two string
with words separated by commas. Try to find what is common
between these strings. The words are not repeated in the
same string.

Your function should find all of the words that appear in
both strings. The result must be represented as a string of
words separated by commas in alphabetic order.

Input: Two arguments as strings.

Output: The common words as a string.

http://www.checkio.org/mission/common-words/

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def checkio(first, second):
    return ','.join(sorted(set(first.split(',')) & set(second.split(','))))

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(u"hello,world", u"hello,earth") == "hello", "Hello"
    assert checkio(u"one,two,three", u"four,five,six") == "", "Too different"
    assert checkio(u"one,two,three", u"four,five,one,two,six,three") == "one,three,two", "1 2 3"
