'''
============================================================
http://projecteuler.net/problem=54

In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:

Hand         Player 1         Player 2         Winner
1         5H 5C 6S 7S KD
Pair of Fives
     2C 3S 8S 8D TD
Pair of Eights
     Player 2
2         5D 8C 9S JS AC
Highest card Ace
     2C 5C 7D 8S QH
Highest card Queen
     Player 1
3         2D 9C AS AH AC
Three Aces
     3D 6D 7D TD QD
Flush with Diamonds
     Player 2
4         4D 6S 9H QH QC
Pair of Queens
Highest card Nine
     3D 6D 7H QD QS
Pair of Queens
Highest card Seven
     Player 1
5         2H 2D 4C 4D 4S
Full House
With Three Fours
     3C 3D 3S 9S 9D
Full House
with Three Threes
     Player 1
The file, poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?
============================================================
'''
import csv

# A convenient enumerated type for the main stat (=rank) of a hand
class Rank: HIGH_CARD, ONE_PAIR, TWO_PAIRS, THREE, STRAIGHT, FLUSH, FULL_HOUSE, FOUR, STRAIGHT_FLUSH, ROYAL_FLUSH = map(str, xrange(10))

# Recode cards to ASCII codes whose ordering preserves card value ordering 
RECODE = dict([(x, x) for x in '23456789'] + [('T', 'A'), ('J', 'B'), ('Q', 'C'), ('K', 'D'), ('A', 'E')])
# Numerical value, for a straight check
NUMERIC_VALUE = dict([(x, int(x)) for x in '23456789'] + [('A', 10), ('B', 11), ('C', 12), ('D', 13), ('E', 14)])
# Rank if a sequence of length >= 2 is found 
LOWEST_RANK_OF_SEQ = [None, None, Rank.ONE_PAIR, Rank.THREE, Rank.FOUR]
# If there's a second pair, mapping between rank before it was found and after 
UPGRADE = {Rank.THREE: Rank.FULL_HOUSE, Rank.ONE_PAIR: Rank.TWO_PAIRS}

class Hand(object):
    '''A data structure representing a poker hand. The hand is internally represented as an recoded
    string of length 5.'''
    
    def __init__(self, hand):
        self._hand = ''.join(sorted((RECODE[c[0]] for c in hand), reverse=True))  # Numerical card values in descending order
        self._flush = all(c[1] == hand[0][1] for c in hand[1:])  # Suits are only relevant for flush determination
    
    @property
    def value(self):
        '''Encode hang's value in a string that preserves the hand value partial-order relation.'''
        rearrange = lambda h, start, L: h[start:start + L] + ''.join(c for k, c in enumerate(h) if k < start or k >= start + L)
        h = self._hand
        start, L = longest_seq(h)
        h = rearrange(h, start, L)
        if L >= 2:
            s = LOWEST_RANK_OF_SEQ[L] + h[0]  # Encode value of longest sequence
            h = h[L:]  # Restrict to a smaller problem: rest of cards in the hand
            start, L = longest_seq(h)
            h = rearrange(h, start, L)
            if L >= 2:  # Found a second pair
                s = UPGRADE[s[0]] + s[1:]
            s += (h[0] + h[L:])  # Encode second pair's value and the remaining cards
        else:  # L = 1, further branching
            straight, flush = is_straight(self._hand), self._flush
            if straight and not flush:
                s = Rank.STRAIGHT + h
            elif not straight and flush:
                s = Rank.FLUSH + h
            elif straight and flush:
                s = Rank.ROYAL_FLUSH if h[0] == 'E' else Rank.STRAIGHT_FLUSH
            else:
                s = Rank.HIGH_CARD + h
        return s.ljust(6, '0')  # Note: '0' < any digit we use
    
def is_straight(h):
    '''Is a hand of straight rank?'''
    h = map(NUMERIC_VALUE.get, h)
    return all(h[k + 1] == h[k] - 1 for k in xrange(len(h) - 1))

def longest_seq(h):
    '''Return start, stop-start of the longest sequence [start,stop) in the list hand.'''
    max_L, n = 0, len(h)
    for start, c in enumerate(h):  # First iteration always sets max_start, max_stop, max_L
        stop = start
        while stop < n and h[stop] == c:
            stop += 1
        L = stop - start
        if L > max_L:
            max_start, max_L = start, L
    return max_start, max_L
    
def compare_hands(h1, h2):
    '''1 if first hand wins, 0 if equal, -1 if second hand wins.''' 
    return cmp(Hand(h1).value, Hand(h2).value)

if __name__ == "__main__":
    # Parse lines and compare them. Count those where the first hand wins. 
    print sum(1 for line in csv.reader(open('problem054.dat', 'rb'), delimiter=' ') if compare_hands(line[0:5], line[5:10]) > 0)
