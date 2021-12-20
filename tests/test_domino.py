from dominoes.domino import Domino


def test_domino_repr():
    domino = Domino(2, 3)
    domino_repr = str(domino)
    assert domino_repr == "Domino(2,3)"
