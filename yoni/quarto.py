'''
============================================================
Quarto game solver.

Created on Apr 11, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
import itertools as it, time

class Quarto(object):
  __LINES__ = [
      [0,1,2,3],
      [4,5,6,7],
      [8,9,10,11],
      [12,13,14,15],
      [0,4,8,12],
      [1,5,9,13],
      [2,6,10,14],
      [3,7,11,15],
      [0,5,10,15],
      [3,6,9,12],
      ]

  __ATTRIBUTES__ = [1,2,4,8]
  UNDECIDED = -2
  __EMPTY__ = -1

  def __init__(self, position, next_player_to_move):
    self.position = position
    self.next_player_to_move = next_player_to_move

  def result(self):
    # Returns the result of the game: 1 if the first player wins, -1 if the
    # second player wins, 0 if a draw, and UNDECIDED if the game is still
    # undecided.

    # Check if there's a four-in-a-row found; if so, the last player to move
    # wins. This is the opponent of the next player to move.
    for line in Quarto.__LINES__:
      if self.four_in_a_row(line): 
#        print line
        return -self.next_player_to_move

    # No four-in-a-row. If board is full, draw. Otherwise, game is undecided.
    return Quarto.UNDECIDED if any(x == Quarto.__EMPTY__ for x in self.position) else 0

  def four_in_a_row(self, line):
    # Returns True if and only if there are four pieces on the line 'line'
    # sharing an attribute.
    pieces = [self.position[location] for location in line]
    return all(piece != Quarto.__EMPTY__ for piece in pieces) and \
    any(all(piece & a for piece in pieces) for a in Quarto.__ATTRIBUTES__)

  def possible_moves(self):
    # Generates all (piece, location) combinations for all legal moves.

    # Generate a mask of the pieces that are not on the board
    # (availability-to-place) and mask of location availability.
    piece_available, location_available = [True] * 16, [False] * 16
    for location, piece in enumerate(self.position):
      if piece != Quarto.__EMPTY__: piece_available[piece] = False
      else: location_available[location] = True
    # Generate all (available piece, available location) combinations.
    for piece, location in \
    it.product([i for i, v in enumerate(piece_available) if v],
               [i for i, v in enumerate(location_available) if v]):
      yield piece, location

class QuartoSolver(object):
  __MAX_DEPTH_TO_PRINT__ = 10

  def __init__(self):
    self.num_positions = 0

  def solve_quarto(self, game=Quarto([-1] * 16, 1), depth=0):
    if depth == 0: self.start_time = time.time()

    if depth <= QuartoSolver.__MAX_DEPTH_TO_PRINT__:
      print ' ' * depth, 'Entering depth', depth
    # Returns the best outcome for the first player (1=win, 0=draw, -1=loss)
    # when the initial position is game.position.

    result = game.result()
    # Leaf node.
#    print game.position, result
    if result != Quarto.UNDECIDED:
      self.num_positions += 1
      return result, 1

    # Non-leaf node, find best result among all children nodes.
    game_with_move_made = Quarto(list(game.position), -game.next_player_to_move)
    best_result = -2
    num_positions = 0
    for piece, location in game.possible_moves():
      # Place the piece 'piece' in the board location 'location'.
      game_with_move_made.position[location] = piece
      # Recurse.
      result, num_positions_in_subtree = self.solve_quarto(game_with_move_made, depth=depth+1)
      num_positions += num_positions_in_subtree
      best_result = max(best_result, result)
      # Undo the move.
      game_with_move_made.position[location] = -1
    if depth <= QuartoSolver.__MAX_DEPTH_TO_PRINT__:
      print ' ' * depth, 'Finished depth', depth, 'best_result', best_result, 'num_positions', num_positions, 'total', self.num_positions, 'hrs/position', (time.time() - self.start_time) / (3600 * self.num_positions)
    return best_result, num_positions

if __name__ == '__main__':
  print QuartoSolver().solve_quarto()
