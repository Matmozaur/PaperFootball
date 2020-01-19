import numpy as np


def get_positions(y, x):
    """
    @param y: y coordinate of line
    @param x: x coordinate of line
    @return: points connected by this line
    """
    position1 = [0, 0]
    position2 = [0, 0]
    position1[1] = x
    if y % 4 == 0:
        position2[1] = x + 1
        position1[0] = int(y / 4)
        position2[0] = int(y / 4)
    elif y % 4 == 1:
        position2[1] = x
        position1[0] = int(y / 4)
        position2[0] = int(y / 4 + 1)
    elif y % 4 == 2:
        position2[1] = x + 1
        position1[0] = int(y / 4)
        position2[0] = int(y / 4) + 1
    elif y % 4 == 3:
        position2[1] = x + 1
        position1[0] = int(y / 4) + 1
        position2[0] = int(y / 4)
    return tuple(position1), tuple(position2)


def get_move(position1, position2):
    """
    @param position1: point before move
    @param position2: point after move
    @return: line between points
    """
    x = min(position1[1], position2[1])
    if position1[1] == position2[1]:
        if position1[0] > position2[0]:
            y = 4 * (position1[0] - 1) + 1
        else:
            y = 4 * position1[0] + 1
    else:
        if position1[0] > position2[0]:
            if position1[1] > position2[1]:
                y = 4 * (position1[0] - 1) + 2
            else:
                y = 4 * (position1[0] - 1) + 3
        elif position1[0] == position2[0]:
            y = 4 * position1[0]
        else:
            if position1[1] < position2[1]:
                y = 4 * position1[0] + 2
            else:
                y = 4 * position1[0] + 3
    return y, x


def get_neighbours(position):
    """
    @param position: given position on the board
    @return: all points to which we can possible move
    """
    neighbours = [(position[0] - 1, position[1] - 1), (position[0] - 1, position[1]),
                  (position[0], position[1] - 1),
                  (position[0] + 1, position[1] + 1), (position[0] + 1, position[1]),
                  (position[0], position[1] + 1),
                  (position[0] + 1, position[1] - 1), (position[0] - 1, position[1] + 1)]
    to_del = []
    for x in neighbours:
        if (x[0] < 0) or (x[0] > 12):
            to_del.append(x)
            continue
        elif (x[1] < 0) or (x[1] > 8):
            to_del.append(x)
        if (position[0] == 12) and (x[0] == 12):
            to_del.append(x)
        if (position[1] == 8) and (x[1] == 8):
            to_del.append(x)

    return [x for x in neighbours if x not in to_del]


def turn_board(board):
    """
    @param board: state of game field
    @return: state of game field from the other player's view
    """
    board2 = np.zeros((48, 8), dtype=int)
    board2[1::4, 0] = 1
    board2[:5, :] = 1
    board2[-4:, :] = 1
    board2[1:5, [3, 4]] = 0
    board2[-5:, [3, 4]] = 0
    board2[1, 3] = 1
    board2[-3, 3] = 1
    for i in range(3, 43):
        for j in range(8):
            if i % 4 == 1:
                if j == 0:
                    board2[i, j] = 1
                else:
                    board2[i, j] = board[46 - i, 8 - j]
            elif i % 4 == 2:
                board2[i + 2, j] = board[46 - i, 7 - j]
            elif i % 4 == 0:
                board2[i + 2, j] = board[46 - i, 7 - j]
            elif i % 4 == 3:
                board2[i + 4, j] = board[46 - i, 7 - j]

    board2[44, 3] = board[4, 4]
    board2[44, 4] = board[4, 3]
    board2[45, 4] = board[1, 4]
    board2[46, 3] = board[2, 4]
    board2[46, 4] = board[2, 3]
    board2[47, 3] = board[3, 4]
    board2[47, 4] = board[3, 3]

    board2[4, 4] = board[44, 3]
    board2[4, 3] = board[44, 4]
    board2[1, 4] = board[45, 4]
    board2[2, 4] = board[46, 3]
    board2[2, 3] = board[46, 4]
    board2[3, 4] = board[47, 3]
    board2[3, 3] = board[47, 4]
    return board2
