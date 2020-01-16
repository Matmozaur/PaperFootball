import copy
import multiprocessing
import time
from random import shuffle
from joblib import Parallel, delayed
from controller import config
from controller.logger import log
from model.game_state_utils import get_positions, get_move, get_neighbours, turn_board


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

    def allowed_actions(self, tmp_board=None, tmp_current_position=None):
        """
        @param tmp_board: state of game field
        @param tmp_current_position: starting position for a move
        @return: all posible lines we can put on the field in that partial move
        """
        if tmp_board is not None and tmp_current_position is not None:
            neighbours = get_neighbours(tmp_current_position)
            allowed = [get_move(tmp_current_position, x) for x in neighbours]
            allowed = [x for x in allowed if tmp_board[x[0], x[1]] == 0]
        else:
            neighbours = get_neighbours(self.current_position)
            allowed = [get_move(self.current_position, x) for x in neighbours]
            allowed = [x for x in allowed if self.board[x[0], x[1]] == 0]
        return allowed

asdfsdf

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

    def get_full_moves_deep(self, max_moves=config.MAX_MOVES, max_final_moves=config.MAX_FINAL_MOVES,
                            max_checked_moves=config.MAX_CHECKED_MOVES):
            """
            @param max_moves: maximal number of moves which will be checked
            @param max_final_moves: maximal number of returned moves
            @param max_checked_moves: maximal number of moves checked while analysing move
            @return: list of possible moves which won't lose game
            """
            start = time.time()
            full_moves = []
            num_cores = multiprocessing.cpu_count()

            def check_for_danger(board, tmp_current_pos, full_moves_final=[]):
                board_temp = turn_board(board)
                tmp_current_pos_turned = (12 - tmp_current_pos[0], 8 - tmp_current_pos[1])
                local_moves = []
                get_full_moves_utils(self, [], board_temp, tmp_current_pos_turned, local_moves,
                                     c_p=tmp_current_pos_turned, max_moves=max_checked_moves, full_moves_final=full_moves_final)
                if len(full_moves_final) >= 1:
                    if full_moves_final[0][2] == 1:
                        return -1
                if len(full_moves_final) > max_final_moves:
                    return -1
                if not local_moves:
                    return 1
                elif local_moves[0][2] == 1:
                    return -1
                return 0

            def go_through_neighbour(self, board, path, neighbour, tmp_current_pos, full_moves, max_moves, full_moves_final=[]):
                tmp_board = copy.deepcopy(board)
                tmp_path = copy.deepcopy(path)
                positions = get_positions(neighbour[0], neighbour[1])
                if positions[0] == tmp_current_pos:
                    x, y = positions[1]
                else:
                    x, y = positions[0]
                tmp_board[neighbour] = 1
                tmp_path.append(neighbour)
                get_full_moves_utils(self, tmp_path, tmp_board, (x, y), full_moves, max_moves=max_moves,
                                     full_moves_final=full_moves_final)

            def get_full_moves_utils(self, path, board, tmp_current_pos, full_moves, c_p=self.current_position, max_moves=max_moves,
                                     full_moves_final=[]):
                if (time.time() - start) >= config.MAX_TIME_CHECKING:
                    return
                if len(full_moves) > max_moves:
                    return
                if len(full_moves_final) > max_final_moves:
                    return
                if len(full_moves_final) >= 1:
                    if full_moves_final[0][2] == 1:
                        return
                if tmp_current_pos != c_p and len(self.allowed_actions(board, tmp_current_pos)) == 7:
                    full_moves.append((path, tmp_current_pos, 0, board))
                    return
                elif tmp_current_pos in {(12, 3), (12, 4), (12, 5)}:
                    return
                if tmp_current_pos in {(0, 3), (0, 4), (0, 5)}:
                    full_moves.clear()
                    full_moves.append((path, tmp_current_pos, 1, board))
                    return
                else:
                    actions = self.allowed_actions(board, tmp_current_pos)
                    shuffle(actions)
                    for neighbour in actions:
                        go_through_neighbour(self, board, path, neighbour, tmp_current_pos, full_moves, max_moves, full_moves_final)

            def check_move(m, full_moves_final):
                if (time.time() - start) >= config.MAX_TIME_CHECKING:
                    return
                if len(full_moves_final) >= max_final_moves:
                    return
                if len(full_moves_final) >= 1:
                    if full_moves_final[0][2] == 1:
                        return
                if m[2] == 1:
                    full_moves_final.clear()
                    full_moves_final.append(m)
                    return
                check = check_for_danger(m[3], m[1], full_moves_final)
                if check == -1:
                    return
                elif check == 1:
                    full_moves_final.clear()
                    full_moves_final.append(m)
                    return
                else:
                    full_moves_final.append(m)

            get_full_moves_utils(self, [], self.board, self.current_position, full_moves)
            end = time.time()
            log('elapsed seconds prepare moves:', end - start)

            start = time.time()
            full_moves_final = []
            shuffle(full_moves)
            Parallel(n_jobs=num_cores, backend="threading")(delayed(check_move)(m, full_moves_final) for m in full_moves)

            end = time.time()
            log('elapsed seconds checking:', end - start)
            log('final_moves', len(full_moves_final))
            return full_moves_final


    def get_full_moves_simple(self, max_moves=config.MAX_MOVES_SIMPLE, max_time=config.MAX_TIME_CHECKING):
        """
            @param max_moves: maximal number of moves which will be checked
            @return: list of possible moves which won't lose game
        """
        start = time.time()
        full_moves = []
        num_cores = multiprocessing.cpu_count()

        def go_through_neighbour(self, board, path, neighbour, tmp_current_pos, full_moves, max_moves, full_moves_final=[]):
            tmp_board = copy.deepcopy(board)
            tmp_path = copy.deepcopy(path)
            positions = get_positions(neighbour[0], neighbour[1])
            if positions[0] == tmp_current_pos:
                x, y = positions[1]
            else:
                x, y = positions[0]
            tmp_board[neighbour] = 1
            tmp_path.append(neighbour)
            self.get_full_moves_utils(self, tmp_path, tmp_board, (x, y), full_moves, max_moves=max_moves,
                                         full_moves_final=full_moves_final)

        def get_full_moves_utils(self, path, board, tmp_current_pos, full_moves, c_p=self.current_position, max_moves=max_moves,
                                    full_moves_final=[]):
            if (time.time() - start) >= max_time:
                return
            if len(full_moves) > max_moves:
                return
            if len(full_moves_final) >= 1:
                if full_moves_final[0][2] == 1:
                    return
            if tmp_current_pos != c_p and len(self.allowed_actions(board, tmp_current_pos)) == 7:
                full_moves.append((path, tmp_current_pos, 0, board))
                return
            elif tmp_current_pos in {(12, 3), (12, 4), (12, 5)}:
                return
            if tmp_current_pos in {(0, 3), (0, 4), (0, 5)}:
                full_moves.clear()
                full_moves.append((path, tmp_current_pos, 1, board))
                return
            else:
                actions = self.allowed_actions(board, tmp_current_pos)
                shuffle(actions)
                for neighbour in actions:
                    self.go_through_neighbour(self, board, path, neighbour, tmp_current_pos, full_moves, max_moves, full_moves_final)

        get_full_moves_utils(self, [], self.board, self.current_position, full_moves)
        end = time.time()
        end = time.time()
        log('elapsed seconds checking:', end - start)
        log('final_moves', len(full_moves))
        return full_moves


    def get_random_move(self, path=[], board=None, tmp_current_pos=None):
        if board == None:
            board = self.board
            tmp_current_pos = self.current_position
        if tmp_current_pos != self.current_position and len(self.allowed_actions(board, tmp_current_pos)) == 7:
            return (path, tmp_current_pos, 0, board)
        elif tmp_current_pos in {(12, 3), (12, 4), (12, 5)}:
            return []
        if tmp_current_pos in {(0, 3), (0, 4), (0, 5)}:
            return (path, tmp_current_pos, 1, board)
        else:
            actions = self.allowed_actions(board, tmp_current_pos)
            shuffle(actions)
            for neighbour in actions:
                x = self.go_through_neighbour(self, board, path, neighbour, tmp_current_pos)
                if len(x) > 0:
                    return x

        def go_through_neighbour(self, board, path, neighbour, tmp_current_pos):
            tmp_board = copy.deepcopy(board)
            tmp_path = copy.deepcopy(path)
            positions = get_positions(neighbour[0], neighbour[1])
            if positions[0] == tmp_current_pos:
                x, y = positions[1]
            else:
                x, y = positions[0]
            tmp_board[neighbour] = 1
            tmp_path.append(neighbour)
            return self.get_full_moves_utils(self, tmp_path, tmp_board, (x, y))

        return []
