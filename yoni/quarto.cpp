// Quarto game solver.
// Created on May 20, 2015
// Author: Oren Livne <oren.livne@gmail.com>
//
// Total number of positions: 6*10^{15}.
// Exploiting symmetries (piece 0, 3 places only at depth 0): 7*10^{13}.
//
// TODO:
// - Memoize positions. If using a weak hash map, prioritize by depth.
// - If found a winning branch when it's his turn, no need to search rest of
//   branches.
// - If first player seems to be losing more than winning, maybe revert to a
//   second-player perspective and apply the previous rule more effectively.
// - Prune branches at move 2 using symmetries.

#include <algorithm>
#include <stdio.h>	// printf
#include <stdlib.h>     // exit, EXIT_FAILURE
#include <vector>

using std::vector;

class Quarto {
 public:
  // Number of squares on the board.
  static const int BOARD_SIZE = 16;
  // Value of an empty square.
  static const char EMPTY = 16 + 1;

  // Game result from the view of the first player to place a piece.
  enum Result { UNDECIDED = -2, LOSS = -1, DRAW = 0, WIN = 1 };
  // Player identifiers.
  enum Player { FIRST = -1, SECOND = 1 };

  // Creates the initial Quarto position.
  Quarto() : Quarto(vector<char>(EMPTY, BOARD_SIZE), FIRST) {}

  // Creates a Quarto position.
  Quarto(const vector<char>& board, Player player_to_move)
      : board_(board), player_to_move_(player_to_move) {
    piece_available_.resize(BOARD_SIZE);
    for (int i = 0; i < BOARD_SIZE; ++i) {
      piece_available_[i] = (board_[i] == EMPTY);
    }
  }

  // Accessors.
  inline const vector<char>& GetBoard() const { return board_; }

  inline const vector<bool>& GetPieceAvailable() const {
    return piece_available_;
  }

  // Returns the result of the game: 1 if the first player wins, -1 if the
  // second player wins, 0 if a draw, and UNDECIDED if the game is still
  // undecided.
  inline Result GetResult() const {
    // Check if there's a quarto; if so, the last player to move wins. This is
    // the opponent of the next player to move.

    if (IsQuarto(board_[0x0], board_[0x1], board_[0x2], board_[0x3]) ||
        IsQuarto(board_[0x4], board_[0x5], board_[0x6], board_[0x7]) ||
        IsQuarto(board_[0x8], board_[0x9], board_[0xa], board_[0xb]) ||
        IsQuarto(board_[0xc], board_[0xd], board_[0xe], board_[0xf]) ||
        IsQuarto(board_[0x0], board_[0x4], board_[0x8], board_[0xc]) ||
        IsQuarto(board_[0x1], board_[0x5], board_[0x9], board_[0xd]) ||
        IsQuarto(board_[0x2], board_[0x6], board_[0xa], board_[0xe]) ||
        IsQuarto(board_[0x3], board_[0x7], board_[0xb], board_[0xf]) ||
        IsQuarto(board_[0x0], board_[0x5], board_[0xa], board_[0xf]) ||
        IsQuarto(board_[0x3], board_[0x6], board_[0x9], board_[0xc])) {
      //printf("Found quarto\n");
      return player_to_move_ == FIRST ? LOSS : WIN;
    }

    // No quarto present. If board is full, draw. Otherwise, game is undecided.
    for (int i = 0; i < BOARD_SIZE; ++i) {
      if (board_[i] == EMPTY) {
        return UNDECIDED;
      }
    }
    return DRAW;
  }

  // Places the piece 'piece' on square number 'square'.
  inline void FillSquare(const char square, const char piece) {
    piece_available_[piece] = false;
    board_[square] = piece;
  }

  // Clears the square number 'square' and makes the piece that was on it available.
  inline void ClearSquare(const char square) {
    piece_available_[board_[square]] = true;
    board_[square] = EMPTY;
  }

  void Print() {
    printf("board: ");
    for (int i = 0; i < BOARD_SIZE; ++i) {
      if (board_[i] == EMPTY) printf("-");
      else printf("%x", board_[i]);
    }
    printf(" piece_available: ");
    for (int i = 0; i < BOARD_SIZE; ++i) {
      printf("%s", piece_available_[i] ? "1" : "0");
    }
    printf("\n");
  }

 private:
  // Returns true if and only if there are pieces on all squares p0,...,p3 that
  // share an attribute ("quarto").
  inline bool IsQuarto(
      const char p0,  const char p1, const char p2, const char p3) const {
    //printf("%x %x %x %x\n", p0, p1, p2, p3);
    // If not all squares are occupied, we can't have a quarto.
    if (p0 == EMPTY || p1 == EMPTY || p2 == EMPTY || p3 == EMPTY) {
      return false;
    }

    // Check all possible attributes for piece attribute equality.
    for (char mask = 0x1; mask <= 0x8; mask <<= 1) {
      const char p0_attribute = p0 & mask;
      //printf("mask %x %x %x %x %x\n", mask, p0_attribute, p1 & mask, p2 & mask, p3 & mask);
      if (((p1 & mask) == p0_attribute) && 
          ((p2 & mask) == p0_attribute) && 
          ((p3 & mask) == p0_attribute)) {
        //printf("Found quarto\n");
        return true;
      }
    }

    return false;
  }

  // Encodes the pieces currently on the board. Pieces are coded as 0-15; an
  // empty square is coded as 16.
  vector<char> board_;
  // A mask that encodes whether each piece is not on the board (pieces are
  // numbered 0-15).
  vector<bool> piece_available_;
  // The next player to place a piece on the board.
  Player player_to_move_;
};

class QuartoSolver {
 public:
  QuartoSolver() : game_(), depth_(0), num_positions_(0L) {}

  // Returns the best outcome for the first player (1=win, 0=draw, -1=loss)
  // starting from the initial position of game.
  inline Quarto::Result Solve() {
#define PAD for (int i = 0; i < depth_; ++i) { printf(" "); }
    // if depth == 0: self.start_time = time.time()
    if (depth_ <= MAX_DEPTH_TO_PRINT) {
      PAD; printf("Entering depth %d\n", depth_);
    }

    //    PAD; game_.Print();
    Quarto::Result result = game_.GetResult();
    //    PAD; printf("result %d\n", result);
    if (result != Quarto::UNDECIDED) {
      // Leaf node.
      ++num_positions_;
      if (depth_ <= MAX_DEPTH_TO_PRINT) {
        PAD; printf("Leaf node at depth %d, result %d, #positions %ld\n", depth_, result, num_positions_);
      }
      return result;
    }

    // Non-leaf node, find best result among all children nodes.
    Quarto::Result best_result = Quarto::UNDECIDED;

    // Consider all (piece, location) combinations for all legal moves.
    // Deep-copy the game board and piece_available arrays because we are
    // modifying game_ in the loop.
    vector<char> board = game_.GetBoard();
    vector<bool> piece_available = game_.GetPieceAvailable();
    if (depth_ == 0) {
      // Optimization: exploit symmetries; without loss of generality, the first
      // placed piece is 0, and it goes on a corner, an edge or a central square.
      printf("Depth 0 optimization\n");
      std::fill(board.begin(), board.end(), 0);
      board[0] = Quarto::EMPTY;
      board[1] = Quarto::EMPTY;
      board[5] = Quarto::EMPTY;
      std::fill(piece_available.begin(), piece_available.end(), false);
      piece_available[0] = true;
    }

    // Traverse the children of the current tree node and find the best result
    // for the first player among them.
    for (char square = 0; square < Quarto::BOARD_SIZE; ++square) {
      if (board[square] == Quarto::EMPTY) {
        for (char piece = 0; piece < Quarto::BOARD_SIZE; ++piece) {
          if (piece_available[piece]) {
            // Place the piece 'piece' in the board location 'square'.
            //            PAD; game_.Print();
            //            PAD; printf("Placing piece %d on square %d\n", piece, square);
            game_.FillSquare(square, piece);
            //            PAD; game_.Print();
            // Recurse.
            ++depth_;
            best_result = std::max(best_result, Solve());
            --depth_;
            // Undo the move.
            //            PAD; game_.Print();
            //            PAD; printf("Clearing square %d\n", square);
            game_.ClearSquare(square);
            //            PAD; game_.Print();
          }
        }
      }
    }

    if (depth_ <= MAX_DEPTH_TO_PRINT) {
      PAD; printf("Finished depth %d, best_result %d, #positions %ld\n", depth_, best_result, num_positions_);
    }
    return best_result;
  }

 private:
  static const int MAX_DEPTH_TO_PRINT = 9;

  Quarto game_;
  int depth_;
  long num_positions_;
};

int main(int argc, char **argv) {
  QuartoSolver solver;
  Quarto::Result best_result = solver.Solve();
  printf("Best game result for first player: %d\n", best_result);
  return 0;
}
