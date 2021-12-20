from enum import Enum

DOMINO_GRID_SIZE = 5


class DominoOrientation(Enum):
    Side1Left = 1
    Side1Down = 2
    Side1Right = 3
    Side1Up = 4


class ConnectionDirection(Enum):
    Left = (-1, 0)
    Down = (0, -1)
    Right = (1, 0)
    Up = (0, 1)


class Graphic:
    def __init__(self, size):
        self.size = size

    def draw_graphic(self):
        raise NotImplementedError


class EmptyGraphic(Graphic):
    def __init__(self, size):
        super().__init__(size)

    def draw_graphic(self):
        # return "-----\n" \
        #       "|   |\n" \
        #       "|   |\n" \
        #       "|   |\n" \
        #       "-----"
        return "     \n" \
               "     \n" \
               "     \n" \
               "     \n" \
               "     \n"


class DominoGraphic(Graphic):
    def __init__(self, val1, val2, orientation, x, y):
        super().__init__(DOMINO_GRID_SIZE)
        self.val1 = val1
        self.val2 = val2
        self.orientation = orientation
        self.x_position = x
        self.y_position = y

    def draw_graphic(self, orientation=None):
        if not orientation:
            orientation = self.orientation
        if orientation == DominoOrientation.Side1Left:
            return "     \n" \
                   "-----\n" \
                   "|{}|{}|\n" \
                   "-----\n" \
                   "     \n".format(self.val1, self.val2)
        elif orientation == DominoOrientation.Side1Up:
            return " --- \n" \
                   " |{}| \n" \
                   " |-| \n" \
                   " |{}| \n" \
                   " --- \n".format(self.val1, self.val2)
        elif orientation == DominoOrientation.Side1Right:
            return "     \n" \
                   "-----\n" \
                   "|{}|{}|\n" \
                   "-----\n" \
                   "     \n".format(self.val2, self.val1)
        elif orientation == DominoOrientation.Side1Down:
            return " --- \n" \
                   " |{}| \n" \
                   " |-| \n" \
                   " |{}| \n" \
                   " --- \n".format(self.val2, self.val1)


class HandGraphic:
    def __init__(self, dominoes):
        self.dominoes = dominoes

    def draw_hand(self):
        domino_graphics = [domino.graphic for domino in self.dominoes]
        for j in range(DOMINO_GRID_SIZE):
            j_row = [graphic.draw_graphic(orientation=DominoOrientation.Side1Up).split('\n')[j] for graphic in domino_graphics]
            print(''.join(j_row))
        print('')

        domino_numbers = list(range(len(self.dominoes)))
        domino_numbers = ["  {}  ".format(num) for num in domino_numbers]
        print(''.join(domino_numbers))


class DominoBoardGraphic:
    def __init__(self, board_size):
        self.full_board = []
        self.board_size = board_size
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        self.init_board()

    def init_board(self):
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                row.append(EmptyGraphic(DOMINO_GRID_SIZE))
            self.full_board.append(row)

    def draw_board(self):
        for i in range(self.y_max, self.y_min - 1, -1):
            row = self.full_board[i][self.x_min:self.x_max + 1]
            for j in range(DOMINO_GRID_SIZE):
                j_row = [graphic.draw_graphic().split('\n')[j] for graphic in row]
                print(''.join(j_row))

    def add_domino(self, domino_graphic):
        x = domino_graphic.x_position
        y = domino_graphic.y_position

        self.full_board[y][x] = domino_graphic
        self.update_min_max(x, y)

    def update_min_max(self, new_x, new_y):
        if self.x_min is None:
            self.x_min = new_x
            self.x_max = new_x
            self.y_min = new_y
            self.y_max = new_y
        else:
            self.y_max = max(self.y_max, new_y)
            self.y_min = min(self.y_min, new_y)
            self.x_max = max(self.x_max, new_x)
            self.x_min = min(self.x_min, new_x)
