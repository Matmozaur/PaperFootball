import numpy as np

from model.game_state import GameState
from model.game_state_utils import turn_board


def empty_board():
    board = np.zeros((48, 8), dtype=int)

    # # board[1::4, 0] = 2
    # # board[:5, :] = 2
    # # board[-5:, :] = 2
    #
    # board[1::4, 0] = 1
    # board[:5, :] = 1
    # board[-5:, :] = 1
    #
    # board[1:5, [3, 4]] = 0
    # board[-5:0, [3, 4]] = 0
    board[1::4, 0] = 1
    board[:5, :] = 1
    board[-4:, :] = 1
    board[1:5, [3, 4]] = 0
    board[-5:, [3, 4]] = 0
    board[1, 3] = 1
    board[-3, 3] = 1
    return board


class Game:

    def __init__(self):
        self.currentPlayer = 1
        self.gameState = GameState(empty_board(), 1, (6, 4))
        self.grid_shape = (48, 8)
        self.input_shape = (2, 48, 8)
        self.name = 'paper_soccer'

    def reset(self):
        self.gameState = GameState(empty_board(), 1, (6, 4))
        self.currentPlayer = 1
        return self.gameState


    # def make_move(self, move):
    #     self.gameState.move(move)


# from article

    def identities(self, state, actionValues):
        identities = [(state, actionValues)]

        currentBoard = state.board
        currentAV = actionValues

        currentBoard = turn_board(currentBoard)

        currentAV = turn_board(currentAV)

        identities.append((GameState(currentBoard, state.playerTurn), currentAV))

        return identities


    # def step(self, action):
    #     next_state, value, done = self.gameState.takeAction(action)
    #     self.gameState = next_state
    #     self.currentPlayer = -self.currentPlayer
    #     info = None
    #     return ((next_state, value, done, info))

    def get_all_allowed_moves(self):
        return self.gameState.get_full_moves()

    def make_move(self, move):
        return self.gameState.make_move(move)

    def change_player(self):
        self.currentPlayer = -self.currentPlayer
        self.gameState.playerTurn = -self.gameState.playerTurn
        self.gameState.board = turn_board(self.gameState.board)
        self.gameState.current_position = (12 - self.gameState.current_position[0], 8 - self.gameState.current_position[1])
