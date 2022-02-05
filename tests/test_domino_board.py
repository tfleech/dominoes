from dominoes.domino import Domino, DominoBoard


def test_root_domino():
    domino = Domino(2, 3)
    board = DominoBoard()

    assert board.dominoes == []
    assert board.endpoints == set()
    assert board.root_domino is None

    board.add_root_domino(domino)

    assert board.dominoes == [domino]
    assert board.root_domino == domino
    assert board.endpoints == {domino.side1, domino.side2}
