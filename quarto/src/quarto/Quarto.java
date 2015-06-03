package quarto;

import java.util.Arrays;

/**
 * A Quarto position. Holds the location of pieces on the board and unused pieces.
 *
 * @author Oren E. Livne {@code <oren.livne@gmail.com>}
 * @version Jun 2, 2015
 */
public final class Quarto {
  // Game result from the view of the first player to place a piece.
  enum Result {
    LOSS(0),
    DRAW(1),
    WIN(2),
    UNDECIDED(3);

    Result(final int value) {
      this.value = value;
    }

    int value() {
      return value;
    }

    private final int value;
  }

  // Player identifiers.
  enum Player {
    FIRST(-1),
    SECOND(1);

    Player(final int value) {
      this.value = value;
    }

    int value() {
      return value;
    }

    public Player opponent() {
      if (this == FIRST)
        return SECOND;
      if (this == SECOND)
        return FIRST;
      throw new InternalError("We shouldn't be here!");
    }

    private final int value;
  }

  // Number of attributes of each piece.
  static final int NUM_ATTRIBUTES = 4;

  // Number of squares on the board.
  static final int BOARD_SIZE = 16;

  // Value of an empty square.
  static final char EMPTY = 16 + 1;

  // Creates the initial Quarto position.
  static Quarto newInstance() {
    final char[] board = new char[BOARD_SIZE];
    Arrays.fill(board, EMPTY);
    return newInstance(board, Player.FIRST);
  }

  // Creates a Quarto position with a given board and player to move.
  static Quarto newInstance(final char[] board, final Player player_to_move) {
    final Quarto quarto = new Quarto();
    quarto.board_ = board;
    quarto.playerToMove_ = player_to_move;

    quarto.pieceAvailable_ = new boolean[BOARD_SIZE];
    Arrays.fill(quarto.pieceAvailable_, true);
    for (int i = 0; i < BOARD_SIZE; ++i) {
      char piece = quarto.board_[i];
      if (piece != EMPTY) {
        quarto.pieceAvailable_[piece] = false;
      }
    }
    return quarto;
  }

  char[] getBoard() {
    return board_;
  }

  boolean[] getPieceAvailable() {
    return pieceAvailable_;
  }

  Player getPlayerToMove() {
    return playerToMove_;
  }

  // Returns the result of the game: 1 if the first player wins, -1 if the
  // second player wins, 0 if a draw, and UNDECIDED if the game is still
  // undecided.
  Result getResult() {
    // Check if there's a quarto; if so, the last player to move wins. This is
    // the opponent of the next player to move.

    if (IsQuarto(board_[0x0], board_[0x1], board_[0x2], board_[0x3])
        || IsQuarto(board_[0x4], board_[0x5], board_[0x6], board_[0x7])
        || IsQuarto(board_[0x8], board_[0x9], board_[0xa], board_[0xb])
        || IsQuarto(board_[0xc], board_[0xd], board_[0xe], board_[0xf])
        || IsQuarto(board_[0x0], board_[0x4], board_[0x8], board_[0xc])
        || IsQuarto(board_[0x1], board_[0x5], board_[0x9], board_[0xd])
        || IsQuarto(board_[0x2], board_[0x6], board_[0xa], board_[0xe])
        || IsQuarto(board_[0x3], board_[0x7], board_[0xb], board_[0xf])
        || IsQuarto(board_[0x0], board_[0x5], board_[0xa], board_[0xf])
        || IsQuarto(board_[0x3], board_[0x6], board_[0x9], board_[0xc])) {
      return playerToMove_ == Player.FIRST ? Result.LOSS : Result.WIN;
    }

    // No quarto present. If board is full, draw. Otherwise, game is undecided.
    for (int i = 0; i < BOARD_SIZE; ++i) {
      if (board_[i] == EMPTY) {
        return Result.UNDECIDED;
      }
    }
    return Result.DRAW;
  }

  // Places the piece 'piece' on square number 'square'.
  void fillSquare(final char square, final char piece) {
    pieceAvailable_[piece] = false;
    board_[square] = piece;
  }

  // Clears the square number 'square' and makes the piece that was on it available.
  void clearSquare(final char square) {
    pieceAvailable_[board_[square]] = true;
    board_[square] = EMPTY;
  }

  void shortPrint() {
    System.out.println("board: ");
    for (int i = 0; i < BOARD_SIZE; ++i) {
      if (board_[i] == EMPTY)
        System.out.println("-");
      else
        System.out.printf("%x", (int) board_[i]);
    }
    System.out.println(" pieceAvailable: ");
    for (int i = 0; i < BOARD_SIZE; ++i) {
      System.out.printf("%s", pieceAvailable_[i] ? "1" : "0");
    }
    System.out.println();
  }

  void print() {
    System.out.println("board: ");
    for (int i = 0; i < BOARD_SIZE; ++i) {
      System.out.printf(" %4s", pieceToString(board_[i]));
      if (i % 4 == 3) {
        System.out.println("");
      }
    }
    System.out.println("pieceAvailable: ");
    for (int i = 0; i < BOARD_SIZE; ++i) {
      System.out.printf("%s", pieceAvailable_[i] ? "1" : "0");
    }
    System.out.println();
  }

  static String pieceToString(char piece) {
    if (piece == EMPTY) {
      return "-";
    } else {
      return String.format("%4s", Integer.toBinaryString(piece)).replace(' ', '0');
    }
  }

  // Returns true if and only if there are pieces on all squares p0,...,p3 that
  // share an attribute ("quarto").
  private boolean IsQuarto(final char p0, final char p1, final char p2, final char p3) {
    // System.out.println("%x %x %x %x\n", p0, p1, p2, p3);
    // If not all squares are occupied, we can't have a quarto.
    if (p0 == EMPTY || p1 == EMPTY || p2 == EMPTY || p3 == EMPTY) {
      return false;
    }

    // Check all possible attributes for piece attribute equality.
    for (char mask = 0x1; mask <= 0x8; mask <<= 1) {
      final int p0_attribute = p0 & mask;
      // System.out.println("mask %x %x %x %x %x\n", mask, p0_attribute, p1 & mask, p2 & mask, p3 &
      // mask);
      if (((p1 & mask) == p0_attribute) && ((p2 & mask) == p0_attribute)
          && ((p3 & mask) == p0_attribute)) {
        // System.out.println("Found quarto\n");
        System.out.printf("Found quarto: %x %x %x %x attribute %x\n", (int) p0, (int) p1, (int) p2,
            (int) p3, (int) mask);
        return true;
      }
    }
    return false;
  }

  // Encodes the pieces currently on the board. Pieces are coded as 0-15; an
  // empty square is coded as 16.
  private char[] board_;

  // A mask that encodes whether each piece is not on the board (pieces are
  // numbered 0-15).
  private boolean[] pieceAvailable_;

  // The next player to place a piece on the board.
  private Player playerToMove_;
}
