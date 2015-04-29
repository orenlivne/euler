'''
============================================================
The Game of Life, also known simply as Life, is a "game" or a cellular automaton devised by the British mathematician John Horton Conway in 1970. The "game" is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves or, for advanced players, by creating patterns with particular properties.
The universe within the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead. Every cell interacts with its eight neighbours, which are cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:
- Any live cell with fewer than two live neighbours dies, as if caused by under-population.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overcrowding.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The initial pattern (or 0th step) constitutes the seed of the
system. The first generation is created by applying the above
rules simultaneously to every cell in the seed-births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick (in other words, each generation is a pure function of the preceding one). The rules continue to be applied repeatedly to create further generations.
In this mission you should count how many live cell will be on the grid at the Nth tick. You are given an initial position (a fragment of the grid with live cells) as a matrix and a number of the tick N. The matrix is represented as a tuple of tuples where 1 is a live cell and 0 is a dead cell. Don't forget that the grid is infinite in each direction.
life
In this example the initial position will be represented as:
((0, 1, 0, 0, 0, 0, 0),
 (0, 0, 1, 0, 0, 0, 0),
 (1, 1, 1, 0, 0, 0, 0),
 (0, 0, 0, 0, 0, 1, 1),
 (0, 0, 0, 0, 0, 1, 1),
 (0, 0, 0, 0, 0, 0, 0),
 (1, 1, 1, 0, 0, 0, 0),)
And if we need to count the live cells for the 4th step, then as we can see from the image above that the answer is 15.
Input: Two arguments. An initial state as a tuple of tuples with integers (0 or 1) and a number for the tick (N) as an integer.
Output: The number of live cell for the Nth tick as an integer.
Precondition: 0 < tick_n < 1000
3 <= len(state) <= 20
all(len(row) == len(state[0]) for row in state)

Created on Apr 19, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from Tkinter import Tk
import ttk

def is_live_at_next_tick(live, (i, j)):
    # Return True if and only cell (i,j) is alive at tick t+1 given the list 'live' of live cells
    # at tick t.
    num_live_nbhrs = sum(1 for k in xrange(i - 1, i + 2) for l in xrange(j - 1, j + 2) if (k != i or l != j) and (k, l) in live)
    return (num_live_nbhrs == 2 or num_live_nbhrs == 3) if (i, j) in live else (num_live_nbhrs == 3)

def life_counter(state, tick_n):
    # Keep a list of the currently live cells.
    live = set((i, j) for i in xrange(len(state)) for j in xrange(len(state[0])) if state[i][j])
    # Step in time.
    for _ in xrange(tick_n):
        # Live cells at next tick = live cells that were live before + live cells that were dead
        # before in neighboring cells of currently live cells
        live = set(cell for cell in live if is_live_at_next_tick(live, cell)) | \
        set((k, l) for (i, j) in live for k in xrange(i - 1, i + 2) for l in xrange(j - 1, j + 2)
            if (k != i or l != j) and (k, l) not in live and is_live_at_next_tick(live, (k, l)))
    # Return the number of live cells at the final tick.
    return len(live)

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert life_counter(((0, 1, 0, 0, 0, 0, 0),
                         (0, 0, 1, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0)), 4) == 15, "Example"
    assert life_counter(((0, 1, 0, 0, 0, 0, 0),
                         (0, 0, 1, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0)), 15) == 14, "Little later"
    assert life_counter(((0, 1, 0),
                         (0, 0, 1),
                         (1, 1, 1)), 50) == 5, "Glider"
    assert life_counter(((1, 1, 0, 1, 1),
                         (1, 1, 0, 1, 1),
                         (0, 0, 0, 0, 0),
                         (1, 1, 0, 1, 1),
                         (1, 1, 0, 1, 1)), 100) == 16, "Stones"

    root = Tk()
    ttk.Button(root, text="Hello World").grid()
    root.mainloop()