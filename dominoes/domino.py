from typing import Optional

from .graphics import (
    ConnectionDirection,
    DominoBoardGraphic,
    DominoGraphic,
    DominoOrientation,
)


class DominoSide:
    def __init__(self, val, domino, connection_direction):
        self.value = val
        self.is_endpoint = False
        self.connection = None
        self.connection_direction = connection_direction
        self.parent_domino: Domino = domino

    def __repr__(self):
        return "{}-Side({})".format(self.parent_domino, self.connection_direction.name)

    def get_playable_value(self):
        return self.value

    def rotate(self, intervals):
        rotations = [
            ConnectionDirection.Left,
            ConnectionDirection.Up,
            ConnectionDirection.Right,
            ConnectionDirection.Down,
        ]
        if self.connection_direction == ConnectionDirection.Left:
            self.connection_direction = rotations[intervals]
        elif self.connection_direction == ConnectionDirection.Down:
            self.connection_direction = rotations[intervals - 1]
        elif self.connection_direction == ConnectionDirection.Right:
            self.connection_direction = rotations[intervals - 2]
        elif self.connection_direction == ConnectionDirection.Up:
            self.connection_direction = rotations[intervals - 3]


class DominoMidSide(DominoSide):
    def __init__(self, domino, connection_direction):
        super().__init__(None, domino, connection_direction)

    def get_playable_value(self):
        return self.parent_domino.side1.value


class Domino:
    def __init__(self, side1_val, side2_val):
        self.side1 = DominoSide(side1_val, self, ConnectionDirection.Left)
        self.side2 = DominoSide(side2_val, self, ConnectionDirection.Right)
        self.orientation = DominoOrientation.Side1Left

        self.graphic = DominoGraphic(side1_val, side2_val, self.orientation, None, None)

    def __repr__(self):
        return "Domino({},{})".format(self.side1.value, self.side2.value)

    def get_playable_sides(self):
        playable_sides = []
        if self.side1.connection is None:
            playable_sides.append(self.side1)
        if self.side2.connection is None:
            playable_sides.append(self.side2)
        return playable_sides

    def get_value_in_play(self):
        return sum([x.value for x in self.get_playable_sides()])

    def rotate(self, intervals):
        # Rotations done clockwise in 90deg intervals
        self.rotate_orientation(intervals)
        self.side1.rotate(intervals)
        self.side2.rotate(intervals)

    def rotate_orientation(self, intervals):
        rotations = [
            DominoOrientation.Side1Left,
            DominoOrientation.Side1Up,
            DominoOrientation.Side1Right,
            DominoOrientation.Side1Down,
        ]
        if self.orientation == DominoOrientation.Side1Left:
            self.orientation = rotations[intervals]
            self.graphic.orientation = rotations[intervals]
        elif self.orientation == DominoOrientation.Side1Down:
            self.orientation = rotations[intervals - 1]
            self.graphic.orientation = rotations[intervals - 1]
        elif self.orientation == DominoOrientation.Side1Right:
            self.orientation = rotations[intervals - 2]
            self.graphic.orientation = rotations[intervals - 2]
        elif self.orientation == DominoOrientation.Side1Up:
            self.orientation = rotations[intervals - 3]
            self.graphic.orientation = rotations[intervals - 3]

    @staticmethod
    def get_rotation_interval(direction1, direction2):
        # we want to align connection directions so:
        # Left -> Right,
        # Find correct alignment with direction1
        alignments = {
            ConnectionDirection.Left: ConnectionDirection.Right,
            ConnectionDirection.Up: ConnectionDirection.Down,
            ConnectionDirection.Right: ConnectionDirection.Left,
            ConnectionDirection.Down: ConnectionDirection.Up,
        }
        goal_alignment = alignments[direction1]

        alignment_map = {
            ConnectionDirection.Left: 1,
            ConnectionDirection.Up: 2,
            ConnectionDirection.Right: 3,
            ConnectionDirection.Down: 4,
        }

        current_alignment = alignment_map[direction2]
        goal_alignment = alignment_map[goal_alignment]
        diff = goal_alignment - current_alignment
        if diff < 0:
            diff += 4

        return diff


class NormalDomino(Domino):
    def __init__(self, side1, side2):
        super().__init__(side1, side2)


class DoubleDomino(Domino):
    def __init__(self, side):
        super().__init__(side, side)
        self.mid_side1 = DominoMidSide(self, ConnectionDirection.Up)
        self.mid_side2 = DominoMidSide(self, ConnectionDirection.Down)

        # Set initial orientation to be vertical
        self.rotate(1)

    def end_sides_available(self):
        return (
            self.mid_side1.connection is not None
            and self.mid_side2.connection is not None
        )

    def get_playable_sides(self):
        playable_sides = []
        if self.end_sides_available():
            if self.side1.connection is None:
                playable_sides.append(self.side1)
            if self.side2.connection is None:
                playable_sides.append(self.side2)
        else:
            if self.mid_side1.connection is None:
                playable_sides.append(self.mid_side1)
            if self.mid_side2.connection is None:
                playable_sides.append(self.mid_side2)
        return playable_sides

    def get_value_in_play(self):
        return 0 if self.end_sides_available() else 2 * self.side1.value

    def rotate(self, intervals):
        self.rotate_orientation(intervals)
        self.side1.rotate(intervals)
        self.side2.rotate(intervals)
        self.mid_side1.rotate(intervals)
        self.mid_side2.rotate(intervals)


class DominoBoard:
    def __init__(self, board_size=100):
        self.root_domino = None
        self.dominoes = []
        self.endpoints = set()

        self.board_graphic = DominoBoardGraphic(board_size)
        self.root_x = int(board_size / 2)
        self.root_y = int(board_size / 2)

    def add_root_domino(self, domino: Domino):
        self.root_domino = domino
        self.dominoes.append(domino)
        new_endpoints = domino.get_playable_sides()
        self.endpoints = self.endpoints.union(set(new_endpoints))

        # Update graphics
        self.root_domino.graphic.x_position = self.root_x
        self.root_domino.graphic.y_position = self.root_y

    def add_leaf_domino(
        self, domino: Domino, endpoint: DominoSide, attachpoint: DominoSide
    ):
        self.dominoes.append(domino)
        self.endpoints.remove(endpoint)
        endpoint_domino = endpoint.parent_domino

        endpoint.connection = attachpoint
        attachpoint.connection = endpoint

        new_endpoints = endpoint_domino.get_playable_sides()
        self.endpoints = self.endpoints.union(set(new_endpoints))
        new_endpoints = domino.get_playable_sides()
        self.endpoints = self.endpoints.union(set(new_endpoints))

        # Update graphics
        endpoint_position = (
            endpoint_domino.graphic.x_position,
            endpoint_domino.graphic.y_position,
        )
        endpoint_direction = endpoint.connection_direction.value
        new_position = (
            endpoint_position[0] + endpoint_direction[0],
            endpoint_position[1] + endpoint_direction[1],
        )
        domino.graphic.x_position = new_position[0]
        domino.graphic.y_position = new_position[1]
        # rotate incoming domino
        rotation_intervals = Domino.get_rotation_interval(
            endpoint.connection_direction, attachpoint.connection_direction
        )
        domino.rotate(rotation_intervals)

    def add_domino(
        self,
        domino: Domino,
        endpoint: Optional[DominoSide] = None,
        attachpoint: Optional[DominoSide] = None,
    ):
        if not self.root_domino:
            self.add_root_domino(domino)
        else:
            if endpoint is None or attachpoint is None:
                assert False, "Need endpoint and attachpoint if not root domino"
            assert endpoint in self.endpoints, "Not a valid endpoint"
            assert (
                endpoint.get_playable_value() == attachpoint.get_playable_value()
            ), "Not a valid move"
            self.add_leaf_domino(domino, endpoint, attachpoint)

        self.board_graphic.add_domino(domino.graphic)

    def get_score(self):
        in_play_dominoes = set([endpoint.parent_domino for endpoint in self.endpoints])
        score = sum([domino.get_value_in_play() for domino in in_play_dominoes])

        return score
