from dominoes.game import DominoBoard, DominoSet

domino_set = DominoSet(max_number=4)

for domino in domino_set.dominoes:
    print(domino)

domino_board = DominoBoard()

print(domino_board.endpoints)
domino_board.add_domino(domino_set.dominoes[1])
print(domino_board.endpoints)
print(domino_board.get_score())
domino_board.board_graphic.draw_board()

next_domino = domino_set.dominoes[5]
endpoint = domino_board.endpoints[1]
attachpoint = next_domino.mid_side1
domino_board.add_domino(next_domino, endpoint, attachpoint)
print(domino_board.endpoints)
print(domino_board.get_score())
domino_board.board_graphic.draw_board()

next_domino = domino_set.dominoes[6]
endpoint = domino_board.endpoints[1]
attachpoint = next_domino.side1
domino_board.add_domino(next_domino, endpoint, attachpoint)
print(domino_board.endpoints)
print(domino_board.get_score())
domino_board.board_graphic.draw_board()

next_domino = domino_set.dominoes[8]
endpoint = domino_board.endpoints[1]
attachpoint = next_domino.side1
domino_board.add_domino(next_domino, endpoint, attachpoint)
print(domino_board.endpoints)
print(domino_board.get_score())
domino_board.board_graphic.draw_board()
