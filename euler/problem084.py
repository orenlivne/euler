'''
============================================================
http://projecteuler.net/problem=84

In the game, Monopoly, the standard board is set up in the following way:

GO    A1    CC1    A2    T1    R1    B1    CH1    B2    B3    JAIL
H2         C1
T2         U1
H1         C2
CH3         C3
R4         R2
G3         D1
CC3         CC2
G2         D2
G1         D3
G2J    F3    U2    F2    F1    R3    E3    E2    CH2    E1    FP
A player starts on the GO square and adds the scores on two 6-sided dice to determine the number of squares they advance in a clockwise direction. Without any further rules we would expect to visit each square with equal probability: 2.5%. However, landing on G2J (Go To Jail), CC (community chest), and CH (chance) changes this distribution.

In addition to G2J, and one card from each of CC and CH, that orders the player to go directly to jail, if a player rolls three consecutive doubles, they do not advance the result of their 3rd roll. Instead they proceed directly to jail.

At the beginning of the game, the CC and CH cards are shuffled. When a player lands on CC or CH they take a card from the top of the respective pile and, after following the instructions, it is returned to the bottom of the pile. There are sixteen cards in each pile, but for the purpose of this problem we are only concerned with cards that order a movement; any instruction not concerned with movement will be ignored and the player will remain on the CC/CH square.

Community Chest (2/16 cards):
Advance to GO
Go to JAIL
Chance (10/16 cards):
Advance to GO
Go to JAIL
Go to C1
Go to E3
Go to H2
Go to R1
Go to next R (railway company)
Go to next R
Go to next U (utility company)
Go back 3 squares.
The heart of this problem concerns the likelihood of visiting a particular square. That is, the probability of finishing at that square after a roll. For this reason it should be clear that, with the exception of G2J for which the probability of finishing on it is zero, the CH squares will have the lowest probabilities, as 5/8 request a movement to another square, and it is the final square that the player finishes at on each roll that we are interested in. We shall make no distinction between "Just Visiting" and being sent to JAIL, and we shall also ignore the rule about requiring a double to "get out of jail", assuming that they pay to get out on their next turn.

By starting at GO and numbering the squares sequentially from 00 to 39 we can concatenate these two-digit numbers to produce strings that correspond with sets of squares.

Statistically it can be shown that the three most popular squares, in order, are JAIL (6.24%) = Square 10, E3 (3.18%) = Square 24, and GO (3.09%) = Square 00. So these three most popular squares can be listed with the six-digit modal string: 102400.

If, instead of using two 6-sided dice, two 4-sided dice are used, find the six-digit modal string.
============================================================
'''
import numpy as np, itertools as it
from scipy.linalg import circulant

class GameAnalysis(object):
    def __init__(self, board):
        self._board = board
        n = len(board)
        self._n = n
        self._A = np.matrix(np.zeros((n, n)))
        self._pad = int(np.log10(n)) + 1
        
    def add_rule(self, rule):
        retval = rule(self._A)  # Rule is applied to A in-place
        if retval is not None: self._A = retval  # Rule is not in-place
        # print rule.__name__
        # print sum(self._A, 0)
    
    def stationary_dist_power_method(self, iters=100):
        '''Approximate, does not require eigen-decomposition.'''
        p, A = np.matrix(np.random.random((self._n, 1))), self._A
        for _ in xrange(iters):
            p = A * p
            p /= sum(p)
        return np.array(p.transpose())[0]

    def stationary_dist(self):
        '''Finds the Perron vector using an eigen-decomposition.'''
        d, v = np.linalg.linalg.eig(self._A)
        p = v[:, np.where(abs(d - 1.0) < 1e-8)[0]]
        p /= sum(p)
        return np.real(np.array(p.transpose())[0])
     
    def modal_str(self, sz):
        p = self.stationary_dist()
        fmt = '%%0%dd' % (self._pad)
        top = np.argsort(p)[self._n - 1:self._n - sz - 1:-1]
        for i in top:
            print 'State %02d p %.16f' % (i, p[i])
        return ''.join(map(lambda x: fmt % (x,), top))

'''Constants - square notation'''
SQUARES = ['GO', 'A1', 'CC1', 'A2', 'T1', 'R1', 'B1', 'CH1', 'B2', 'B3',
           'JAIL', 'C1', 'U1', 'C2', 'C3', 'R2', 'D1', 'CC2', 'D2', 'D3',
           'FP', 'E1', 'CH2', 'E2', 'E3', 'R3', 'F1', 'F2', 'U2', 'F3', 'G2J',
           'G1', 'G2', 'CC3', 'G3', 'R4', 'CH3', 'H1', 'T2', 'H2']

'''Square->number mapping.'''
S = dict((v, k) for (k, v) in enumerate(SQUARES))

'''Card series'''
series = lambda prefix: filter(lambda x: x.startswith(prefix), SQUARES)
CC, CH = series('CC'), series('CH')
next_in_series = lambda i, prefix : it.dropwhile(lambda y: not y.startswith(prefix), SQUARES[i + 1:] + SQUARES[:i - 1]).next()
next_in_series_dict = lambda cards, prefix: dict((x, next_in_series(S[x], prefix)) for x in cards)
NEXT_R, NEXT_U = next_in_series_dict(CH, 'R'), next_in_series_dict(CH, 'U')

'''Monopoly Rules'''
def rule_advance(A, dice_sides):
    '''Note: dice_sides must not exceed the board''s capacity.'''
    prob = np.array([0] * 2 + range(1, dice_sides + 1) + range(dice_sides - 1, 0, -1) + 
                    [0] * (A.shape[0] - (2 * dice_sides + 1))) / float(dice_sides ** 2)
    return circulant(prob)

def rule_g2j(A):
    A[S['JAIL']] += A[S['G2J']]
    A[S['G2J']] = 0
    
def rule_consecutive_doubles(A, dice_sides, turns):
    n = A.shape[0]
    e, u = np.matrix(np.zeros((n, 1))), np.matrix(np.ones((n, 1)))
    e[S['JAIL']] = 1.0
    p = 1.0 / (dice_sides ** turns)
    return (1 - p) * A + p * e * u.transpose()

def rule_card(A, squares, num_cards, go_to_cards):
    norm = 1.0 / float(num_cards)
    for x in squares:
        i = S[x]
        Ai = A[i] * norm
        go_to = map(S.get, go_to_cards(x))
        for y in go_to: A[y] += Ai
        A[i] *= (1.0 - len(go_to) * norm)
        # print '\t', 'x', x, 'i', i, 'go_to', go_to,
        # print '\t\t', sum(A, 0)

rule_cc = lambda A: rule_card(A, CC, 16, lambda _: ['GO', 'JAIL'])
rule_ch = lambda A: rule_card(A, CH, 16, lambda x: ['GO', 'JAIL', 'C1', 'E3', 'H2',
                                                    'R1', NEXT_R[x], NEXT_R[x], NEXT_U[x],
                                                    SQUARES[(S[x] - 3) % A.shape[0]]])
 
def monopoly(dice_sides, turns):
    game = GameAnalysis(S)
    game.add_rule(lambda A: rule_advance(A, dice_sides))
    game.add_rule(rule_g2j)
    game.add_rule(rule_cc)
    game.add_rule(rule_ch)
    game.add_rule(lambda A: rule_consecutive_doubles(A, dice_sides, turns))
    return game

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    np.set_printoptions(threshold=np.nan, linewidth=500)
    print monopoly(6, 3).modal_str(3)
    print monopoly(4, 3).modal_str(3)
