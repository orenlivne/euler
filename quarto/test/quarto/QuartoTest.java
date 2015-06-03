package quarto;

import org.junit.Assert;
import org.junit.Test;

import java.util.Arrays;

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
      Assert.assertEquals(Quarto.EMPTY, board[i]);
      Assert.assertTrue(pieceAvailable[i]);
    }
  }

  @Test
  public void instanceWithBoardSetsMembersCorrectly() {
    char[] board = {0, 1, Quarto.EMPTY, 3, 15, 14, 13, 12, 4, 5, 6, 7, 11, Quarto.EMPTY, 9, 8};

    Quarto quarto = Quarto.newInstance(board, Quarto.Player.SECOND);
    Assert.assertArrayEquals(board, quarto.getBoard());
    Assert.assertEquals(Quarto.Player.SECOND, quarto.getPlayerToMove());

    boolean[] expectedPiecesAvailable = new boolean[Quarto.BOARD_SIZE];
    Arrays.fill(expectedPiecesAvailable, false);
    expectedPiecesAvailable[2] = true;
    expectedPiecesAvailable[10] = true;
    assertArrayEquals(expectedPiecesAvailable, quarto.getPieceAvailable());
  }

  /**
   * Asserts that two byte arrays are equal. If they are not, an
   * {@link AssertionError} is thrown.
   *
   * @param expecteds byte array with expected values.
   * @param actuals byte array with actual values
   */
  public static void assertArrayEquals(boolean[] expecteds, boolean[] actuals) {
    Assert.assertEquals(expecteds.length, actuals.length);
    for (int i = 0; i < expecteds.length; i++) {
      Assert.assertEquals(
          "Difference at index " + i + ": expected " + expecteds[i] + " actual " + actuals[i],
          expecteds[i], actuals[i]);
    }
  }
}
