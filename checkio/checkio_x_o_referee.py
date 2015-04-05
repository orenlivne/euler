class Game(object):
    def __init__(self, board):
        self.board = board

    def row(self, i):
        return self.board[i]

    def col(self, j):
        return [self.board[i][j] for i in xrange(len(self.board))]

    def diag1(self):
        return [self.board[i][i] for i in xrange(self.board)]

    def diag2(self):
        n = self.board
        return [self.board[i][n-1-i] for i in xrange(n)]

    def line_winner(self, line):
        return line[0] if all(line[i] == line[i+1] for i in xrange(len(line)-1)) and line[0] != '.' else '.'

    def winner(self):
        for i in xrange(len(self.board)):
            w = self.line_winner(self.row(i))
            if w != '.': return w
        for j in xrange(len(self.board[0])):
            w = self.line_winner(self.col(j))
            if w != '.': return w
        for d  in [self.diag1(), self.diag2()]:
            w = self.line_winner(d)
            if w != '.': return w
        return 'D'

def checkio(game_result):
    return Game(game_result).winner()

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio([
        u"X.O",
        u"XX.",
        u"XOO"]) == "X", "Xs wins"
    assert checkio([
        u"OO.",
        u"XOX",
        u"XOX"]) == "O", "Os wins"
    assert checkio([
        u"OOX",
        u"XXO",
        u"OXX"]) == "D", "Draw"
    assert checkio([
        u"O.X",
        u"XX.",
        u"XOO"]) == "X", "Xs wins again"

