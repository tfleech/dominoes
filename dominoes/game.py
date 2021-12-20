from random import sample

from .domino import DominoBoard, DoubleDomino, NormalDomino
from .graphics import HandGraphic


class DominoSet:
    def __init__(self, min_number=0, max_number=6):
        self.dominoes = []
        for i in range(min_number, max_number + 1, 1):
            for j in range(i, max_number + 1, 1):
                if i == j:
                    self.dominoes.append(DoubleDomino(i))
                else:
                    self.dominoes.append(NormalDomino(i, j))

    def draw_hand(self, hand_size):
        selected_dominoes = sample(self.dominoes, hand_size)
        for domino in selected_dominoes:
            self.dominoes.remove(domino)
        return Hand(selected_dominoes)

    def draw_single(self):
        selected_domino = sample(self.dominoes, 1)[0]
        self.dominoes.remove(selected_domino)
        return selected_domino

    def draw_fixed_hand(self, idxs):
        selected_dominoes = []
        for idx in idxs:
            selected_dominoes.append(self.dominoes[idx])
        for domino in selected_dominoes:
            self.dominoes.remove(domino)
        return Hand(selected_dominoes)


class Hand:
    def __init__(self, dominoes):
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

    def get_domino_by_index(self, domino_index):
        return self.dominoes[domino_index]

    def remove_domino(self, domino):
        self.dominoes.remove(domino)

    def add_domino(self, domino):
        self.dominoes.append(domino)


class GameOnePlayer:
    def __init__(self):
        self.domino_set = DominoSet()
        self.board = DominoBoard()
        self.player_hand = self.domino_set.draw_hand(7)
        # self.player_hand = self.domino_set.draw_fixed_hand([18, 21, 26, 20, 19, 23, 24])

    def check_valid_moves(self):
        board_playable_values = [endpoint.get_playable_value() for endpoint in self.board.endpoints]
        hand_playable_values = self.player_hand.get_playable_values()
        for i in board_playable_values:
            for j in hand_playable_values:
                if i == j:
                    return True
        return False

    def play(self):
        self.player_hand.hand_graphic.draw_hand()
        selected_domino = int(input("What domino do you want to start with? "))
        selected_domino = self.player_hand.get_domino_by_index(selected_domino)
        self.board.add_domino(selected_domino)
        self.player_hand.remove_domino(selected_domino)
        self.board.board_graphic.draw_board()
        print(self.board.endpoints)
        print(self.board.get_score())

        while True:
            self.player_hand.hand_graphic.draw_hand()
            if not self.check_valid_moves():
                print("You have to go to the bone pile")
                draw = self.domino_set.draw_single()
                self.player_hand.add_domino(draw)
                self.board.board_graphic.draw_board()
                print(self.board.endpoints)
                print(self.board.get_score())
                continue

            selected_domino = int(input("What domino do you want to play next? "))
            selected_domino = self.player_hand.get_domino_by_index(selected_domino)
            selected_endpoint = int(input("Where do you want to play it? "))
            selected_endpoint = self.board.endpoints[selected_endpoint]

            if isinstance(selected_domino, DoubleDomino):
                attachpoint = selected_domino.mid_side1
                if attachpoint.get_playable_value() != selected_endpoint.get_playable_value():
                    print("Not a valid move, please try again")
                    print("")
                    continue
            elif isinstance(selected_domino, NormalDomino):
                if selected_domino.side1.value == selected_endpoint.get_playable_value():
                    attachpoint = selected_domino.side1
                elif selected_domino.side2.value == selected_endpoint.get_playable_value():
                    attachpoint = selected_domino.side2
                else:
                    print("Not a valid move, please try again")
                    print("")
                    continue

            # TODO: keep track of score
            self.board.add_domino(selected_domino, selected_endpoint, attachpoint)

            self.player_hand.remove_domino(selected_domino)

            self.board.board_graphic.draw_board()
            print(self.board.endpoints)
            print(self.board.get_score())
