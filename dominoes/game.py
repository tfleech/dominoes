from random import randint, sample

from .domino import Domino, DominoBoard, DoubleDomino
from .player import Hand, Player


class DominoSet:
    def __init__(self, min_number=0, max_number=6):
        self.dominoes = []
        for i in range(min_number, max_number + 1, 1):
            for j in range(i, max_number + 1, 1):
                if i == j:
                    self.dominoes.append(DoubleDomino(i))
                else:
                    self.dominoes.append(Domino(i, j))

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


class GameTwoPlayer:
    def __init__(self, player1: Player, player2: Player):
        self.domino_set = DominoSet()
        self.board = DominoBoard()
        self.players = [player1, player2]
        self.turn = randint(0, 1)

        # TODO: make configurable
        self.show_hands = [True, True]

        for player in self.players:
            player.draw_new_hand(self.domino_set.draw_hand(7))

    def bone_pile(self, player: Player):
        while len(player.get_possible_moves(self.board)) == 0:
            if len(self.domino_set.dominoes) == 0:
                return
            new_domino = self.domino_set.draw_single()
            player.hand.add_domino(new_domino)

    def print_scores(self):
        for player in self.players:
            print("{}: {}".format(player.name, player.score))

    def play(self):

        while True:
            turn_player = self.players[self.turn]
            if self.show_hands[self.turn]:
                print(turn_player.name)
                turn_player.hand.hand_graphic.draw_hand()
            # import pdb; pdb.set_trace()

            if len(turn_player.get_possible_moves(self.board)) == 0:
                self.bone_pile(turn_player)
                if self.show_hands[self.turn]:
                    turn_player.hand.hand_graphic.draw_hand()

            move = turn_player.choose_next_move(self.board)
            self.board.add_domino(
                move.domino_to_play, move.side_on_board, move.side_to_play
            )
            turn_player.hand.remove_domino(move.domino_to_play)

            score = self.board.get_score()
            if score % 5 == 0:
                turn_player.score += score // 5

            self.board.board_graphic.draw_board()
            self.print_scores()

            if isinstance(move.domino_to_play, DoubleDomino) or score % 5 == 0:
                continue

            if len(turn_player.hand.dominoes) == 0:
                leftover_points = max(
                    sum([player.hand.get_total_value() for player in self.players])
                    // 5,
                    1,
                )
                turn_player.score += leftover_points
                self.print_scores()
                print("Game Over")
                break

            self.turn = (self.turn + 1) % len(self.players)


class GameOnePlayer:
    def __init__(self):
        self.domino_set = DominoSet()
        self.board = DominoBoard()
        self.player_hand = self.domino_set.draw_hand(7)
        # self.player_hand = self.domino_set.draw_fixed_hand([18, 21, 26, 20, 19, 23, 24])

    def check_valid_moves(self):
        board_playable_values = [
            endpoint.get_playable_value() for endpoint in self.board.endpoints
        ]
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
            selected_endpoint = list(self.board.endpoints)[selected_endpoint]

            if isinstance(selected_domino, DoubleDomino):
                attachpoint = selected_domino.mid_side1
                if (
                    attachpoint.get_playable_value()
                    != selected_endpoint.get_playable_value()
                ):
                    print("Not a valid move, please try again")
                    print("")
                    continue
            elif isinstance(selected_domino, Domino):
                if (
                    selected_domino.side1.value
                    == selected_endpoint.get_playable_value()
                ):
                    attachpoint = selected_domino.side1
                elif (
                    selected_domino.side2.value
                    == selected_endpoint.get_playable_value()
                ):
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
