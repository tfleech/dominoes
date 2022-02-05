from dominoes.game import GameTwoPlayer
from dominoes.player import Hand, HumanPlayer, RandomPlayer

player1 = RandomPlayer(Hand([]), name="player1")
# player2 = RandomPlayer(Hand([]), name='player2')
player2 = HumanPlayer(Hand([]), name="IAmHuman")

game = GameTwoPlayer(player1=player1, player2=player2)
game.play()

# hand = domino_set.draw_hand(7)
# hand.hand_graphic.draw_hand()

# domino_board = DominoBoard()
