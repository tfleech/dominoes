from dominoes.domino import DominoOrientation
from dominoes.graphics import DominoBoardGraphic, DominoGraphic

board = DominoBoardGraphic(2)

# board.draw_board()

domino_graphic = DominoGraphic(2, 3, DominoOrientation.Side1Left, 0, 0)
board.full_board[0][0] = domino_graphic
board.draw_board()
