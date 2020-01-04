from controller.playing import play_valid
from model.game import empty_board
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
board[44, 3] = 1
boardGUI = BoardGui()
boardGUI.draw_board(board)
