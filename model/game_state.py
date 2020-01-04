import numpy as np

from controller import config


class GameState:
    """
    Class responsible for logic side of the game.
    Positions are tuples (x,y) where x is integer from 0 to 12 and y from 0 to 8, they indicates points on the field.
    Lines are tuples (x,y) where x is integer from 0 to 48 and y from 0 to 8, they indicates lines on the field.
    Lines differs regarding to x%4, 0:_ 1: | 2: \  3: /
    """
    def __init__(self, board, player_turn, current_position):
        """
        @param board: current state of game field
        @param player_turn: current player (-1, 1)
        @param current_position: current position of the ball
        """
        self.board = board
        self.playerTurn = player_turn
        self.current_position = current_position

    @staticmethod
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

    def allowed_actions(self, tmp_board=None, tmp_current_position=None):
        """
        @param tmp_board: state of game field
        @param tmp_current_position: starting position for a move
        @return: all posible lines we can put on the field in that partial move
        """
        if tmp_board is not None and tmp_current_position is not None:
            neighbours = self.get_neighbours(tmp_current_position)
            allowed = [self.get_move(tmp_current_position, x) for x in neighbours]
            allowed = [x for x in allowed if tmp_board[x[0], x[1]] == 0]
        else:
            neighbours = self.get_neighbours(self.current_position)
            allowed = [self.get_move(self.current_position, x) for x in neighbours]
            allowed = [x for x in allowed if self.board[x[0], x[1]] == 0]
        return allowed

    # def move(self, position):
    #     a, b = self.get_move(self.current_position, position)
    #     if (a, b) in self._allowed_actions():
    #         self.board[a, b] = 1
    #         self.current_position = position
    #     else:
    #         print('Error, wrong move')

    # def check_for_end_game(self):
    #     if len(self.allowed_actions()) == 0:
    #         return -1
    #     if self.current_position[0] == 12:
    #         return -1
    #     if self.current_position[0] == 0:
    #         return 1
    #     return 0

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    def get_full_moves(self):
        full_moves = []

        def check_for_danger(board, tmp_current_pos):
            board_temp = GameState.turn_board(board)
            tmp_current_pos_turned = (12 - tmp_current_pos[0], 8 - tmp_current_pos[1])
            # print(board, tmp_current_pos)
            local_moves = []
            get_full_moves_utils(self, [], board_temp, tmp_current_pos_turned, local_moves, safety=False, c_p=tmp_current_pos_turned)
            print([(p[0], p[1], p[2]) for p in local_moves])
            if not local_moves:
                return 1
            elif local_moves[0][2] == 1:
                return -1
            return 0

        def get_full_moves_utils(self, path, board, tmp_current_pos, full_moves, safety=True, c_p=self.current_position):
            if len(full_moves) >config.max_t:
                return
            if tmp_current_pos != c_p and len(self.allowed_actions(board, tmp_current_pos)) == 7:
                if safety:
                    print('checks move:', path)
                    checker = check_for_danger(board, tmp_current_pos)
                    if checker == -1:
                        return
                    if checker == 1:
                        full_moves.append((path, tmp_current_pos, 1, board))
                        return
                full_moves.append((path, tmp_current_pos, 0, board))
                return
            elif tmp_current_pos in {(12, 3), (12, 4), (12, 5)}:
                return
            if tmp_current_pos in {(0, 3), (0, 4), (0, 5)}:
                full_moves.clear()
                full_moves.append((path, tmp_current_pos, 1, board))
            # print(self._allowed_actions(board,tmp_current_pos))
            else:
                for neighbour in self.allowed_actions(board, tmp_current_pos):
                    tmp_board = board.copy()
                    tmp_path = path.copy()
                    positions = self.get_positions(neighbour[0], neighbour[1])
                    if positions[0] == tmp_current_pos:
                        x, y = positions[1]
                    else:
                        x, y = positions[0]

                    # print(x,y)
                    tmp_board[neighbour] = 1
                    tmp_path.append(neighbour)
                    # print('tmp_path: ', tmp_path)
                    # print('tmp_board: ', tmp_board)
                    # print('tmp_current_pos: ', tmp_current_pos)
                    # print('neighbour: ', neighbour)

                    get_full_moves_utils(self, tmp_path, tmp_board, (x, y), full_moves, safety=safety)

        get_full_moves_utils(self, [], self.board, self.current_position, full_moves)
        return full_moves

    def make_move(self, move):
        """
        Ok
        Applies move to game enviroment
        @param move: move to apply (lines, new current point, result, new board)
        @return: done and result
        """
        # print(move)
        if move is None:
            return 1, -1
        if len(move) == 0:
            return 1, -1
        self.current_position = move[1]
        for line in move[0]:
            self.board[line[0], line[1]] = 1
        done = 1
        if move[2] == 0:
            done = 0
        return done, move[2]


# # from article
#     def _allowedActions(self, allowed = [], path = []):
#         for a in self.get_neighbours(self.current_position):
#             if a not in path:
#                 if len(self.get_neighbours(a)) == 7:
#                     path.append(a)
#                     allowed.append(path)
#                 else:
#                     path.append(a)
#                     allowed += self._allowedActions(self, allowed = allowed, path = path)
#         return allowed


# def _binary(self):
#
# 	currentplayer_position = np.zeros(len(self.board), dtype=np.int)
# 	currentplayer_position[self.board==self.playerTurn] = 1
#
# 	other_position = np.zeros(len(self.board), dtype=np.int)
# 	other_position[self.board==-self.playerTurn] = 1
#
# 	position = np.append(currentplayer_position,other_position)
#
# 	return (position)
#
# def _convertStateToId(self):
# 	player1_position = np.zeros(len(self.board), dtype=np.int)
# 	player1_position[self.board==1] = 1
#
# 	other_position = np.zeros(len(self.board), dtype=np.int)
# 	other_position[self.board==-1] = 1
#
# 	position = np.append(player1_position,other_position)
#
# 	id = ''.join(map(str,position))
#
# 	return id
#
# def _checkForEndGame(self):
# 	if np.count_nonzero(self.board) == 42:
# 		return 1
#
# 	for x,y,z,a in self.winners:
# 		if (self.board[x] + self.board[y] + self.board[z] + self.board[a] == 4 * -self.playerTurn):
# 			return 1
# 	return 0
#
#
# def _getValue(self):
# 	# This is the value of the state for the current player
# 	# i.e. if the previous player played a winning move, you lose
# 	for x,y,z,a in self.winners:
# 		if (self.board[x] + self.board[y] + self.board[z] + self.board[a] == 4 * -self.playerTurn):
# 			return (-1, -1, 1)
# 	return (0, 0, 0)
#
#
# def _getScore(self):
# 	tmp = self.value
# 	return (tmp[1], tmp[2])
#
#
#
#
# def takeAction(self, action):
# 	newBoard = np.array(self.board)
# 	newBoard[action]=self.playerTurn
#
# 	newState = GameState(newBoard, -self.playerTurn)
#
# 	value = 0
# 	done = 0
#
# 	if newState.isEndGame:
# 		value = newState.value[0]
# 		done = 1
#
# 	return (newState, value, done)
