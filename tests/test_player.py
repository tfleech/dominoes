from dominoes.domino import Domino, DominoBoard, DoubleDomino
from dominoes.player import Hand, Move, Player, RandomPlayer


def test_get_possible_moves():
    dominoes = [Domino(2, 3), Domino(3, 4), DoubleDomino(2), Domino(3, 5)]
    hand = Hand(dominoes[:3])
    player = Player(hand)

    board = DominoBoard()

    moves = player.get_possible_moves(board)
    assert moves == [Move(domino) for domino in dominoes[:3]]

    board.add_domino(dominoes[3])

    moves = player.get_possible_moves(board)

    assert Move(dominoes[0], dominoes[0].side2, dominoes[3].side1) in moves
    assert Move(dominoes[1], dominoes[1].side1, dominoes[3].side1) in moves


def test_random_make_move():
    dominoes = [Domino(2, 3), DoubleDomino(2), Domino(3, 5)]
    hand = Hand(dominoes[:2])
    player = RandomPlayer(hand)

    board = DominoBoard()
    board.add_domino(dominoes[2])

    move = player.choose_next_move(board)
    assert move == Move(dominoes[0], dominoes[0].side2, dominoes[2].side1)

    player = RandomPlayer(Hand([dominoes[1]]))
    move = player.choose_next_move(board)
    assert move.is_pass_move is True
