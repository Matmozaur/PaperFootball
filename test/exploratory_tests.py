from controller.playing import play_valid
from model.game import empty_board, Game
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import *
import pickle

from view.board import Board
from view.board_gui import BoardGui

"""
Playing matches between 2 bots
"""

# file = open('../controller/temp_fw_trained', 'rb')
# b = pickle.load(file)
# player1 = Agent('random_player', RandomModel())
# player2 = Agent('forward_player',  ForwardModel())
# player3 = Agent('backward_player',  BackwardModel())
# sc1 = play_valid(player1, b, episodes=10)
# sc2 = play_valid(player2, b, episodes=50, random_moves=2)
# print(sc1)
# print(sc2)
# sc = play_valid(player3, b, episodes=10)
# print(sc)


"""
Visualising board
"""
board = empty_board()
board[26, 4] = 1
board[30, 5] = 1
board[33, 6] = 1
board[38, 6] = 1
board[37, 7] = 1
board[36, 7] = 1
board[39, 7] = 1
board[34, 7] = 1
boardGUI = BoardGui()
boardGUI.draw_board(board)




# game = Game()
# board = game.gameState.board.copy()
# board[26, 4] = 1
# board[30, 5] = 1
# board[33, 6] = 1
# board[38, 6] = 1
# board[37, 7] = 1
# board[36, 7] = 1
# allowed = {(39, 7), (34, 7)}
# game.gameState.allowed_actions(board, (9, 8))
