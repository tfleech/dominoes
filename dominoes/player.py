from typing import List, Optional

from .domino import Domino, DominoBoard, DominoSide, DoubleDomino
from .graphics import HandGraphic


class Move:
    def __init__(
        self,
        domino_to_play: Optional[Domino] = None,
        side_to_play: Optional[DominoSide] = None,
        side_on_board: Optional[DominoSide] = None,
    ):
        self.domino_to_play = domino_to_play
        self.side_to_play = side_to_play
        self.side_on_board = side_on_board

        self.is_pass_move = False
        if self.domino_to_play is None:
            self.is_pass_move = True

        assert (side_to_play is None) == (
            side_on_board is None
        ), "Tried to create invalid move"

    def __eq__(self, other):
        if (
            self.side_to_play == other.side_to_play
            and self.side_on_board == other.side_on_board
        ):
            return True
        return False


class Hand:
    def __init__(self, dominoes: List[Domino]):
        self.dominoes = dominoes
        self.hand_graphic = HandGraphic(dominoes)

    def get_playable_values(self):
        playable_values = []
        for domino in self.dominoes:
            if isinstance(domino, DoubleDomino):
                playable_values.append(domino.mid_side1.get_playable_value())
            else:
                playable_values.append(domino.side1.value)
                playable_values.append(domino.side2.value)
        return playable_values

    def get_sides(self):
        sides = []
        for domino in self.dominoes:
            sides.extend(domino.get_playable_sides())
        return sides

    def get_total_value(self):
        sides = self.get_sides()
        return sum([side.get_playable_value() for side in sides])

    def get_domino_by_index(self, domino_index: int):
        return self.dominoes[domino_index]

    def remove_domino(self, domino: Domino):
        self.dominoes.remove(domino)

    def add_domino(self, domino: Domino):
        self.dominoes.append(domino)


class Player:
    def __init__(self, hand: Hand, name: str = "player"):
        self.hand = hand
        self.name = name
        self.score = 0

    def get_possible_moves(self, board: DominoBoard) -> List[Move]:
        sides_in_hand: List[DominoSide] = self.hand.get_sides()
        board_endpoints: List[DominoSide] = board.endpoints

        # If first move, return all dominoes in hand
        if len(board_endpoints) == 0:
            return [Move(domino_to_play=domino) for domino in self.hand.dominoes]

        moves = []
        for side in sides_in_hand:
            for endpoint in board_endpoints:
                if side.get_playable_value() == endpoint.get_playable_value():
                    moves.append(Move(side.parent_domino, side, endpoint))
        return moves

    def draw_new_hand(self, hand: Hand):
        self.hand = hand

    def choose_next_move(self, board: DominoBoard):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, hand: Hand, name: str = "player"):
        super().__init__(hand, name)

    def choose_next_move(self, board: DominoBoard):
        moves = self.get_possible_moves(board)
        if len(moves) > 0:
            return moves[0]
        else:
            return Move()


class HumanPlayer(Player):
    def __init__(self, hand: Hand, name: str = "player"):
        super().__init__(hand, name)

    def choose_next_move(self, board: DominoBoard):
        selected_domino_idx = int(input("What domino do you want to play next? "))
        selected_domino = self.hand.get_domino_by_index(selected_domino_idx)

        if len(board.endpoints) == 0:
            return Move(selected_domino)

        print(board.endpoints)
        selected_endpoint_idx = int(input("Where do you want to play it? "))
        selected_endpoint = list(board.endpoints)[selected_endpoint_idx]

        if isinstance(selected_domino, DoubleDomino):
            attachpoint = selected_domino.mid_side1
            if (
                attachpoint.get_playable_value()
                != selected_endpoint.get_playable_value()
            ):
                print("Not a valid move, please try again")
                print("")
                return self.choose_next_move(board)
            else:
                return Move(selected_domino, attachpoint, selected_endpoint)
        elif isinstance(selected_domino, Domino):
            if selected_domino.side1.value == selected_endpoint.get_playable_value():
                attachpoint = selected_domino.side1
                return Move(selected_domino, attachpoint, selected_endpoint)
            elif selected_domino.side2.value == selected_endpoint.get_playable_value():
                attachpoint = selected_domino.side2
                return Move(selected_domino, attachpoint, selected_endpoint)
            else:
                print("Not a valid move, please try again")
                print("")
                return self.choose_next_move(board)
