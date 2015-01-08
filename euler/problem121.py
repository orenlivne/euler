'''
============================================================
http://projecteuler.net/problem=121

A bag contains one red disc and one blue disc. In a game of chance a player takes a disc at random and its colour is noted. After each turn the disc is returned to the bag, an extra red disc is added, and another disc is taken at random.

The player pays $1 to play and wins if they have taken more blue discs than red discs at the end of the game.

If the game is played for four turns, the probability of a player winning is exactly 11/120, and so the maximum prize fund the banker should allocate for winning in this game would be $10 before they would expect to incur a loss. Note that any payout will be a whole number of pounds and also includes the original $1 paid to play the game, so in the example given the player actually wins $9.

Find the maximum prize fund that should be allocated to a single game in which fifteen turns are played.
============================================================
'''
import numpy as np

def max_prize(num_turns):
    p_old, p_new = np.zeros((num_turns + 1,)), np.zeros((num_turns + 1,))
    p_old[0] = 1.0
    for n in xrange(1, num_turns + 1):
        p_new.fill(0.0)
        p = p_old[:n]
        p_new[:n] += (n / (n + 1.)) * p
        p_new[1:n + 1] += (1. / (n + 1.)) * p
        p_old[:] = p_new[:]
    return int(1. / sum(p_old[int(np.ceil(0.5 * (num_turns + 1))):]))

if __name__ == "__main__":
    print max_prize(4)
    print max_prize(15)
