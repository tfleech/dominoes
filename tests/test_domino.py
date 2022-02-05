from dominoes.domino import Domino, DominoSide, DoubleDomino
from dominoes.graphics import ConnectionDirection, DominoOrientation


def test_domino_repr():
    domino = Domino(2, 3)
    domino_repr = str(domino)
    assert domino_repr == "Domino(2,3)"


def test_domino_sides():
    domino = Domino(2, 3)

    assert isinstance(domino.side1, DominoSide)
    assert isinstance(domino.side2, DominoSide)
    assert domino.side1.value == 2
    assert domino.side2.value == 3


def test_domino_starting_orientation():
    domino = Domino(2, 3)

    assert domino.orientation == DominoOrientation.Side1Left
    assert domino.side1.connection_direction == ConnectionDirection.Left
    assert domino.side2.connection_direction == ConnectionDirection.Right


def test_get_playable_sides():
    domino = Domino(2, 3)
    domino2 = Domino(3, 4)

    playable_sides = domino.get_playable_sides()
    assert playable_sides == [domino.side1, domino.side2]

    domino.side2.connection = domino2.side1
    domino2.side1.connection = domino.side2

    playable_sides = domino.get_playable_sides()
    assert playable_sides == [domino.side1]


def test_get_value_in_play():
    domino = Domino(2, 3)
    domino2 = Domino(3, 4)

    value_in_play = domino.get_value_in_play()
    assert value_in_play == 5

    domino.side2.connection = domino2.side1
    domino2.side1.connection = domino.side2

    value_in_play = domino.get_value_in_play()
    assert value_in_play == 2


def test_get_rotation_interval():
    assert (
        Domino.get_rotation_interval(ConnectionDirection.Left, ConnectionDirection.Left)
        == 2
    )
    assert (
        Domino.get_rotation_interval(ConnectionDirection.Left, ConnectionDirection.Down)
        == 3
    )
    assert (
        Domino.get_rotation_interval(
            ConnectionDirection.Right, ConnectionDirection.Left
        )
        == 0
    )
    assert (
        Domino.get_rotation_interval(
            ConnectionDirection.Right, ConnectionDirection.Right
        )
        == 2
    )


def test_rotate_orientation():
    domino = Domino(2, 3)

    domino.rotate_orientation(1)
    assert domino.orientation == DominoOrientation.Side1Up

    domino.rotate_orientation(2)
    assert domino.orientation == DominoOrientation.Side1Down

    domino.rotate_orientation(3)
    assert domino.orientation == DominoOrientation.Side1Right


def test_rotate():
    domino = Domino(2, 3)

    domino.rotate(1)
    assert domino.orientation == DominoOrientation.Side1Up
    assert domino.side1.connection_direction == ConnectionDirection.Up
    assert domino.side2.connection_direction == ConnectionDirection.Down


def test_double_domino():
    domino = DoubleDomino(2)

    assert domino.side1.value == 2
    assert domino.side2.value == 2
    assert domino.mid_side1.value is None
    assert domino.mid_side2.value is None

    assert domino.orientation == DominoOrientation.Side1Up
    assert domino.mid_side1.connection_direction == ConnectionDirection.Right
    assert domino.mid_side2.connection_direction == ConnectionDirection.Left


def test_double_playable_sides():
    domino = DoubleDomino(2)
    domino2 = Domino(2, 3)
    domino3 = Domino(2, 4)
    domino4 = Domino(2, 5)

    playable_sides = domino.get_playable_sides()
    assert playable_sides == [domino.mid_side1, domino.mid_side2]

    domino.mid_side1.connection = domino2.side1
    playable_sides = domino.get_playable_sides()
    assert playable_sides == [domino.mid_side2]

    domino.mid_side2.connection = domino3.side1
    playable_sides = domino.get_playable_sides()
    assert playable_sides == [domino.side1, domino.side2]

    domino.side1.connection = domino4.side1
    playable_sides = domino.get_playable_sides()
    assert playable_sides == [domino.side2]


def test_double_get_value_in_play():
    domino = DoubleDomino(2)
    domino2 = Domino(2, 3)
    domino3 = Domino(2, 4)
    domino4 = Domino(2, 5)

    value_in_play = domino.get_value_in_play()
    assert value_in_play == 4

    domino.mid_side1.connection = domino2.side1
    value_in_play = domino.get_value_in_play()
    assert value_in_play == 4

    domino.mid_side2.connection = domino3.side1
    value_in_play = domino.get_value_in_play()
    assert value_in_play == 0

    domino.side1.connection = domino4.side1
    value_in_play = domino.get_value_in_play()
    assert value_in_play == 0


def test_double_rotate():
    domino = DoubleDomino(2)

    domino.rotate(1)
    assert domino.orientation == DominoOrientation.Side1Right
    assert domino.side1.connection_direction == ConnectionDirection.Right
    assert domino.side2.connection_direction == ConnectionDirection.Left
    assert domino.mid_side1.connection_direction == ConnectionDirection.Down
    assert domino.mid_side2.connection_direction == ConnectionDirection.Up

    domino.rotate(3)
    assert domino.orientation == DominoOrientation.Side1Up
    assert domino.side1.connection_direction == ConnectionDirection.Up
    assert domino.side2.connection_direction == ConnectionDirection.Down
    assert domino.mid_side1.connection_direction == ConnectionDirection.Right
    assert domino.mid_side2.connection_direction == ConnectionDirection.Left
