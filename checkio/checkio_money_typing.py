'''
============================================================
The infinite monkey theorem states that a monkey hitting keys at random on a typewriter keyboard for an infinite length of time will almost surely type out a given text, such as the complete works of John Wallis, or more likely, a Dan Brown novel.

Let's suppose our monkeys are typing, typing and typing, and have produced a wide variety of short text segments. Let's try to check them for sensible word inclusions.

You are given some text potentially including sensible words. You should count how many words are included in the given text. A word should be whole and may be a part of other word. Text letter case does not matter. Words are given in lowercase and don't repeat. If a word appears several times in the text, it should be counted only once.

For example, text - "How aresjfhdskfhskd you?", words - ("how", "are", "you", "hello"). The result will be 3.

Input: Two arguments. A text as a string (unicode for py2) and words as a set of strings (unicode for py2).

Output: The number of words in the text as an integer.

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import re

def count_words(text, words):
    patterns = dict([(word, re.compile('.*%s.*' % (word,))) for word in words])
    for token in (x.lower() for x in text.split()):
        appearing_words = [word for word, pattern in patterns.iteritems() if pattern.match(token)]
        for word in appearing_words: del patterns[word]
        if not patterns: break
    return len(words) - len(patterns)

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert count_words('LOLOLOLOLOL', {'lol', 'olo'}) == 2, "Intersecting words"
    assert count_words("How aresjfhdskfhskd you?", {"how", "are", "you", "hello"}) == 3, "Example"
    assert count_words("Bananas, give me bananas!!!", {"banana", "bananas"}) == 2, "BANANAS!"
    assert count_words("Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
                       {"sum", "hamlet", "infinity", "anything"}) == 1, "Weird text"
    
    
