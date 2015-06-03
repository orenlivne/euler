package quarto;

import static quarto.Quarto.EMPTY;

import org.junit.Assert;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Quarto board unit tests.
 */
public class QuartoTest {
  @Test
  public void defaultInstanceReturnsEmptyBoard() {
    Quarto quarto = Quarto.newInstance();
    char[] board = quarto.getBoard();
    boolean[] pieceAvailable = quarto.getPieceAvailable();
    Assert.assertEquals(Quarto.BOARD_SIZE, board.length);
    Assert.assertEquals(Quarto.Player.FIRST, quarto.getPlayerToMove());
    Assert.assertEquals(Quarto.BOARD_SIZE, pieceAvailable.length);

    for (int i = 0; i < Quarto.BOARD_SIZE; i++) {
      Assert.assertEquals(EMPTY, board[i]);
      Assert.assertTrue(pieceAvailable[i]);
    }
  }

  @Test
  public void instanceWithBoardSetsMembersCorrectly() {
    char[] board = {
        0, 1, EMPTY, 3, //
        15, 14, 13, 12, //
        4, 5, 6, 7, //
        11, EMPTY, 9, 8,
    };

    Quarto quarto = Quarto.newInstance(board, Quarto.Player.SECOND);
    Assert.assertArrayEquals(board, quarto.getBoard());
    Assert.assertEquals(Quarto.Player.SECOND, quarto.getPlayerToMove());

    boolean[] expectedPiecesAvailable = new boolean[Quarto.BOARD_SIZE];
    Arrays.fill(expectedPiecesAvailable, false);
    expectedPiecesAvailable[2] = true;
    expectedPiecesAvailable[10] = true;
    assertArrayEquals(expectedPiecesAvailable, quarto.getPieceAvailable());
  }

  @Test
  public void getResultConclusiveForFirstRow() {
    // Attributes 2 and 3 match for the first row.
    char[] board = {
        0, 1, 2, 3, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForSecondRow() {
    char[] board = {
        EMPTY, EMPTY, EMPTY, EMPTY, //
        0, 1, 2, 3, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForThirdRow() {
    char[] board = {
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        0, 1, 2, 3, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForFourthRow() {
    char[] board = {
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        0, 1, 2, 3,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForFirstColumn() {
    char[] board = {
        0, EMPTY, EMPTY, EMPTY, //
        1, EMPTY, EMPTY, EMPTY, //
        2, EMPTY, EMPTY, EMPTY, //
        3, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForSecondColumn() {
    char[] board = {
        EMPTY, 0, EMPTY, EMPTY, //
        EMPTY, 1, EMPTY, EMPTY, //
        EMPTY, 2, EMPTY, EMPTY, //
        EMPTY, 3, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForThirdColumn() {
    char[] board = {
        EMPTY, EMPTY, 0, EMPTY, //
        EMPTY, EMPTY, 1, EMPTY, //
        EMPTY, EMPTY, 2, EMPTY, //
        EMPTY, EMPTY, 3, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForFourthColumn() {
    char[] board = {
        EMPTY, EMPTY, EMPTY, 0, //
        EMPTY, EMPTY, EMPTY, 1, //
        EMPTY, EMPTY, EMPTY, 2, //
        EMPTY, EMPTY, EMPTY, 3,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForLeftDiagonal() {
    char[] board = {
        0, EMPTY, EMPTY, EMPTY, //
        EMPTY, 1, EMPTY, EMPTY, //
        EMPTY, EMPTY, 2, EMPTY, //
        EMPTY, EMPTY, EMPTY, 3,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForRightDiagonal() {
    char[] board = {
        EMPTY, EMPTY, EMPTY, 0, //
        EMPTY, EMPTY, 1, EMPTY, //
        EMPTY, 2, EMPTY, EMPTY, //
        3, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
  }

  @Test
  public void getResultConclusiveForFirstAttribute() {
    // Attribute 0, value = 0 in all pieces.
    char[] board = {
        0, 2, 4, 6, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);

    // Attribute 0, value = 1 in all pieces.
    char[] board2 = {
        1, 3, 5, 7, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board2);
  }

  @Test
  public void getResultConclusiveForSecondAttribute() {
    // Attribute 1, value = 0 in all pieces.
    char[] board = {
        0, 4, 12, 13, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);

    // Attribute 1, value = 1 in all pieces.
    char[] board2 = {
        10, 2, 3, 6, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board2);
  }

  @Test
  public void getResultConclusiveForThirdAttribute() {
    // Attribute 2, value = 0 in all pieces.
    char[] board = {
        0, 2, 8, 9, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
    // Attribute 2, value = 1 in all pieces.
    char[] board2 = {
        15, 12, 4, 7, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board2);
  }

  @Test
  public void getResultConclusiveForFourthAttribute() {
    // Attribute 3, value = 0 in all pieces.
    char[] board = {
        0, 1, 3, 7, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board);
    // Attribute 3, value = 1 in all pieces.
    char[] board2 = {
        8, 9, 14, 15, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY,
    };
    testGetResultCorrectForConclusiveBoard(board2);
  }

  @Test
  public void getResultUndecidedFullRowNoAttributes() {
    // Attribute 3, value = 0 in all pieces.
    char[] board = {
        0, 15, 3, 12, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        EMPTY, EMPTY, EMPTY, EMPTY, //
        1, 2, 4, 8,
    };
    testGetResultReturnsExpectedResult(board, Quarto.Result.UNDECIDED);
  }

  @Test
  public void getResultDrawForDrawnBoard() {
    char[] board = {
        9, 8, 14, 4, //
        0, 11, 10, 13, //
        12, 6, 5, 3, //
        15, 1, 7, 2,
    };

    testGetResultReturnsExpectedResult(board, Quarto.Result.DRAW);
    assertBoardIsFull(board);
  }

  @Test
  public void getResultDrawForRandomDrawnBoard() {
    Quarto quarto = generateRandomBoardWithResult(Quarto.Result.DRAW);
    testGetResultReturnsExpectedResult(quarto.getBoard(), Quarto.Result.DRAW);
    assertBoardIsFull(quarto.getBoard());
  }

  private void assertBoardIsFull(char[] board) {
    Quarto quarto = Quarto.newInstance(board, Quarto.Player.FIRST);
    boolean[] pieceAvailable = quarto.getPieceAvailable();
    for (int i = 0; i < Quarto.BOARD_SIZE; i++) {
      Assert.assertNotEquals(EMPTY, board[i]);
      Assert.assertFalse(pieceAvailable[i]);
    }
  }

  private void testGetResultCorrectForConclusiveBoard(char[] board) {
    Quarto quarto = Quarto.newInstance(board, Quarto.Player.FIRST);
    Assert.assertEquals(Quarto.Result.LOSS, quarto.getResult());

    quarto = Quarto.newInstance(board, Quarto.Player.SECOND);
    Assert.assertEquals(Quarto.Result.WIN, quarto.getResult());
  }

  private void testGetResultReturnsExpectedResult(char[] board, Quarto.Result expectedResult) {
    Quarto quarto = Quarto.newInstance(board, Quarto.Player.FIRST);
    Assert.assertEquals(expectedResult, quarto.getResult());

    quarto = Quarto.newInstance(board, Quarto.Player.SECOND);
    Assert.assertEquals(expectedResult, quarto.getResult());
  }

  /**
   * Asserts that two byte arrays are equal. If they are not, an
   * {@link AssertionError} is thrown.
   *
   * @param expecteds byte array with expected values.
   * @param actuals byte array with actual values
   */
  private static void assertArrayEquals(boolean[] expecteds, boolean[] actuals) {
    Assert.assertEquals(expecteds.length, actuals.length);
    for (int i = 0; i < expecteds.length; i++) {
      Assert.assertEquals(
          "Difference at index " + i + ": expected " + expecteds[i] + " actual " + actuals[i],
          expecteds[i], actuals[i]);
    }
  }

  private static Quarto generateRandomBoardWithResult(Quarto.Result result) {
    char[] board = null;
    while (true) {
      List<Character> list = new ArrayList<Character>();
      for (char i = 0; i < 16; i++) {
        list.add(i);
      }
      java.util.Collections.shuffle(list);
      board = new char[16];
      for (char i = 0; i < 16; i++) {
        board[i] = list.get(i);
      }
      Quarto quarto = Quarto.newInstance(board, Quarto.Player.FIRST);
      if (quarto.getResult() == result) {
        return quarto;
      }
    }
  }
}
