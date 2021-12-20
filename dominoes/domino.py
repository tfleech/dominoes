from typing import Optional

from .graphics import (ConnectionDirection, DominoBoardGraphic, DominoGraphic,
                       DominoOrientation)


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
        rotations = [ConnectionDirection.Left, ConnectionDirection.Up, ConnectionDirection.Right, ConnectionDirection.Down]
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

    def rotate(self, intervals):
        # Rotations done clockwise in 90deg intervals
        self.rotate_orientation(intervals)
        self.side1.rotate(intervals)
        self.side2.rotate(intervals)

    def rotate_orientation(self, intervals):
        rotations = [DominoOrientation.Side1Left, DominoOrientation.Side1Up, DominoOrientation.Side1Right, DominoOrientation.Side1Down]
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
        alignments = {ConnectionDirection.Left: ConnectionDirection.Right,
                      ConnectionDirection.Up: ConnectionDirection.Down,
                      ConnectionDirection.Right: ConnectionDirection.Left,
                      ConnectionDirection.Down: ConnectionDirection.Up}
        goal_alignment = alignments[direction1]

        alignment_map = {ConnectionDirection.Left: 1,
                         ConnectionDirection.Up: 2,
                         ConnectionDirection.Right: 3,
                         ConnectionDirection.Down: 4}

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

    def end_sides_available(self):
        return self.mid_side1.connection is not None and self.mid_side2.connection is not None

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
        self.endpoints = []

        self.board_graphic = DominoBoardGraphic(board_size)
        self.root_x = int(board_size / 2)
        self.root_y = int(board_size / 2)

    def add_root_domino(self, domino: Domino):
        self.root_domino = domino
        self.dominoes.append(domino)
        if isinstance(domino, NormalDomino):
            self.endpoints.append(domino.side1)
            self.endpoints.append(domino.side2)
        elif isinstance(domino, DoubleDomino):
            self.endpoints.append(domino.mid_side1)
            self.endpoints.append(domino.mid_side2)
            domino.rotate(1)

        self.root_domino.graphic.x_position = self.root_x
        self.root_domino.graphic.y_position = self.root_y
        self.board_graphic.add_domino(self.root_domino.graphic)
        return

    def add_leaf_domino(self, domino: Domino, endpoint: DominoSide, attachpoint: DominoSide):
        self.dominoes.append(domino)
        self.endpoints.remove(endpoint)
        endpoint_domino = endpoint.parent_domino

        endpoint.connection = attachpoint
        attachpoint.connection = endpoint

        # Update endpoints if double domino just got completed
        if isinstance(endpoint_domino, DoubleDomino) and isinstance(endpoint, DominoMidSide):
            if endpoint_domino.end_sides_available():
                if endpoint_domino.side1.connection is None:
                    self.endpoints.append(endpoint_domino.side1)
                if endpoint_domino.side2.connection is None:
                    self.endpoints.append(endpoint_domino.side2)

        # Update endpoints if double domino just got played
        if isinstance(domino, DoubleDomino):
            if attachpoint == domino.mid_side1:
                self.endpoints.append(domino.mid_side2)
            if attachpoint == domino.mid_side2:
                self.endpoints.append(domino.mid_side1)

        # Update endpoints if normal domino just got played
        if isinstance(domino, NormalDomino):
            if attachpoint == domino.side1:
                self.endpoints.append(domino.side2)
            if attachpoint == domino.side2:
                self.endpoints.append(domino.side1)

        # Update graphics
        endpoint_position = (endpoint_domino.graphic.x_position, endpoint_domino.graphic.y_position)
        endpoint_direction = endpoint.connection_direction.value
        new_position = (endpoint_position[0] + endpoint_direction[0], endpoint_position[1] + endpoint_direction[1])
        domino.graphic.x_position = new_position[0]
        domino.graphic.y_position = new_position[1]
        # rotate incoming domino
        rotation_intervals = Domino.get_rotation_interval(endpoint.connection_direction, attachpoint.connection_direction)
        domino.rotate(rotation_intervals)

    def add_domino(self, domino: Domino, endpoint: Optional[DominoSide] = None, attachpoint: Optional[DominoSide] = None):
        if not self.root_domino:
            self.add_root_domino(domino)
        else:
            if endpoint is None or attachpoint is None:
                assert False, 'Need endpoint and attachpoint if not root domino'
            assert endpoint in self.endpoints, 'Not a valid endpoint'
            assert endpoint.get_playable_value() == attachpoint.get_playable_value(), 'Not a valid move'
            self.add_leaf_domino(domino, endpoint, attachpoint)

        self.board_graphic.add_domino(domino.graphic)

    def get_score(self):
        # Basically sum all the endpoints of normal dominoes
        # special treatment for endpoints of doubles
        score = 0
        for endpoint in self.endpoints:
            endpoint_domino = endpoint.parent_domino
            if isinstance(endpoint_domino, NormalDomino):
                score += endpoint.get_playable_value()
            elif isinstance(endpoint_domino, DoubleDomino):
                if isinstance(endpoint, DominoMidSide):
                    score += 2 * endpoint.get_playable_value()
                elif isinstance(endpoint, DominoSide):
                    continue

        return score
