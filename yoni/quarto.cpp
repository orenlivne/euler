// Quarto game solver.
// Created on May 20, 2015
// Author: Oren Livne <oren.livne@gmail.com>

#include <algorithm>
#include <stdio.h>		// printf
#include <stdlib.h>     // exit, EXIT_FAILURE

class Quarto {
public:
	// Game result from the view of the first player to place a piece.
	enum Result { UNDECIDED = -2, LOSS = -1, DRAW = 0, WIN = 1 };
	enum Player { FIRST = -1, SECOND = 1 };
	
	// Allows encoding and easily accessing the pieces on the board.
	// Each square is a 4-bit group in a 64-bit long integer. Its value encodes
	// the occupying piece (0-15), one bit per one of the four binary piece attributes.
	// If a square is empty, its value in this struct is ignored.
	typedef union {
		unsigned long value;
		struct { unsigned b0:4, b1:4, b2:4, b3:4, b4:4, b5:4, b6:4, b7:4,
						  b8:4, b9:4, ba:4, bb:4, bc:4, bd:4, be:4, bf:4; } piece;
	} Board;

	// A mask that encodes the status of each square in a collection of 16 squares (or pieces).
	typedef union {
		unsigned short value;
		struct { unsigned b0:1, b1:1, b2:1, b3:1, b4:1, b5:1, b6:1, b7:1,
						  b8:1, b9:1, ba:1, bb:1, bc:1, bd:1, be:1, bf:1; } bit;
	} SquareStatus;
	
	// Creates the initial Quarto position.
	/*Quarto(const long board, const short empty, const Player player_to_move) :
		board_({board}), empty_({empty}), player_to_move_(player_to_move) {
		piece_available_ = {0xff};
		long b = board;
		for (int i = 0; i < 16; ++i) {
			piece_available_.value &= ~(1 << (b & 0x4));
			b >>= 4;
		}
	}*/
	Quarto() : board_({0}), empty_({0xff}), piece_available_({0xff}), player_to_move_(Quarto::Player::FIRST) {}

	// Accessors.
	inline short GetBoard() const { return board_.value; }
	inline short GetEmpty() const { return empty_.value; }
	inline short GetPieceAvailable() const { return piece_available_.value; }
	
    // Returns the result of the game: 1 if the first player wins, -1 if the
    // second player wins, 0 if a draw, and UNDECIDED if the game is still undecided.
	inline Result GetResult() const {
		// Check if there's a quarto; if so, the last player to move wins. This is the
		// opponent of the next player to move.
		
#define IS_QUARTO(p0, p1, p2, p3) \
		if (!empty_.bit.b##p0 && !empty_.bit.b##p1 && !empty_.bit.b##p2 && !empty_.bit.b##p3 && \
			IsQuarto(board_.piece.b##p0, board_.piece.b##p1, board_.piece.b##p2, board_.piece.b##p3)) { \
			return Result(-player_to_move_); \
		}
				
		IS_QUARTO(0, 1, 2, 3);
		IS_QUARTO(4, 5, 6, 7);
		IS_QUARTO(8, 9, a, b);
		IS_QUARTO(c, d, e, f);
		IS_QUARTO(0, 4, 8, c);
		IS_QUARTO(1, 5, 9, d);
		IS_QUARTO(2, 6, a, e);
		IS_QUARTO(3, 7, b, f);
		IS_QUARTO(0, 5, a, f);
		IS_QUARTO(3, 6, 9, c);

#undef IS_QUARTO
	  
		// No quarto present. If board is full, draw. Otherwise, game is undecided.
		return (empty_.value == 0) ? Result::DRAW : Result::UNDECIDED;
	}	
 	
	// Places the piece 'piece' on square number 'square'.
	inline void FillSquare(const short square, const short piece) {
		empty_.value &= ~(1 << square);
		piece_available_.value &= ~(1 << piece);
	
		switch (square) {
			case 0x0: { board_.piece.b0 = piece; break; }
			case 0x1: { board_.piece.b1 = piece; break; }
			case 0x2: { board_.piece.b2 = piece; break; }
			case 0x3: { board_.piece.b3 = piece; break; }
			case 0x4: { board_.piece.b4 = piece; break; }
			case 0x5: { board_.piece.b5 = piece; break; }
			case 0x6: { board_.piece.b6 = piece; break; }
			case 0x7: { board_.piece.b7 = piece; break; }
			case 0x8: { board_.piece.b8 = piece; break; }
			case 0x9: { board_.piece.b9 = piece; break; }
			case 0xa: { board_.piece.ba = piece; break; }
			case 0xb: { board_.piece.bb = piece; break; }
			case 0xc: { board_.piece.bc = piece; break; }
			case 0xd: { board_.piece.bd = piece; break; }
			case 0xe: { board_.piece.be = piece; break; }
			case 0xf: { board_.piece.bf = piece; break; }
			default: { printf("We shouldn't be here!"); exit(EXIT_FAILURE); }
		}
	}	
	
	// Clears the square number 'square' and makes the piece that was on it available.
	inline void ClearSquare(const short square) {
		const short piece = (board_.value >> (4 * square)) & 0x4;
		empty_.value |= (1 << square);
		piece_available_.value |= (1 << piece);
		// Don't bother unsetting the board location since the corresponding empty entry
		// (set to true here) guards against using it.
	}	

	// Returns true if and only if the game position is to be considered for processing by
	// the solver. Optimization that utilizes symmetries of the constraints to reduce the number
	// of position we have to look at.
	inline bool isCanonicalPosition() const {
		return true;
	}
	
private:
    // Returns true if and only if there are pieces on all squares p0,...,p3 that share
	// an attribute.
	inline bool IsQuarto(const short p0,  const short p1, const short p2, const short p3) const {
		for (short mask = 0x1; mask <= 0x8; mask <<= 1) {
			const int p0_attribute = p0 & mask;
			if ((p1 & mask == p0_attribute) ||
				(p2 & mask == p0_attribute) || 
				(p3 & mask == p0_attribute)) {
				return true;
			}
		}
		return false;
	}
	
	// Encodes the pieces currently on the board.
	Board board_;
	// A mask that encodes which board squares (0-15) are empty.
	SquareStatus empty_;
	// A mask that encodes whether each piece is on the board or not(pieces are numbered 0-15).
	SquareStatus piece_available_;
	// The next player to place a piece on the board.
	Player player_to_move_;
};

class QuartoSolver {
public:
	QuartoSolver() : game_(), depth_(0), num_positions_(0L) {}

	// Returns the best outcome for the first player (1=win, 0=draw, -1=loss) starting from
	// the initial position of game.
	inline Quarto::Result Solve() {
#define PAD for (int i = 0; i < depth_; ++i) { printf(" "); }
		// if depth == 0: self.start_time = time.time()
		if (depth_ <= MAX_DEPTH_TO_PRINT) {
			PAD; printf("Entering depth %d\n", depth_);
		}

		Quarto::Result result = game_.GetResult();
		PAD; printf("board: %016lx empty: %02x piece_available: %02x\n", game_.GetBoard(), game_.GetEmpty(), game_.GetPieceAvailable());
		PAD; printf("result %d\n", result);
		if (result != Quarto::Result::UNDECIDED) {
			// Leaf node.
			++num_positions_;
			return result;
		}
		
		// Non-leaf node, find best result among all children nodes.
		Quarto::Result best_result = Quarto::Result::UNDECIDED;

		// Consider all (piece, location) combinations for all legal moves.
		short empty = game_.GetEmpty();
		for (short square = 0; square < 16; ++square) {
			if (empty & 0x1) {
				short piece_available = game_.GetPieceAvailable();
				for (short piece = 0; piece < 16; ++piece) {
					if (piece_available & 0x1) {
						// Place the piece 'piece' in the board location 'square'.
						PAD; printf("board: %016lx empty: %02x piece_available: %02x\n", game_.GetBoard(), game_.GetEmpty(), game_.GetPieceAvailable());
						PAD; printf("Placing piece %d on square %d\n", piece, square);
						game_.FillSquare(square, piece);
						PAD; printf("board: %016lx empty: %02x piece_available: %02x\n", game_.GetBoard(), game_.GetEmpty(), game_.GetPieceAvailable());
						// Recurse.
						if (game_.isCanonicalPosition()) {
							++depth_;
							Quarto::Result result = Solve();
							best_result = std::max(best_result, result);
							--depth_;
						}
						// Undo the move.
						PAD; printf("board: %016lx empty: %02x piece_available: %02x\n", game_.GetBoard(), game_.GetEmpty(), game_.GetPieceAvailable());
						PAD; printf("Clearing square %d\n", square);
						game_.ClearSquare(square);
						PAD; printf("board: %016lx empty: %02x piece_available: %02x\n", game_.GetBoard(), game_.GetEmpty(), game_.GetPieceAvailable());
					}
					piece_available >>= 1;
				}
			}
			empty >>= 1;
		}		
	  
		if (depth_ <= MAX_DEPTH_TO_PRINT) {
			PAD; printf("Finished depth %d, best_result %d, #positions %ld\n", depth_, best_result, num_positions_);
		}
		return best_result;
	}

private:
	static const int MAX_DEPTH_TO_PRINT = 10;

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
