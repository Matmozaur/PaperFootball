import time

from controller.logger import log
from controller.playing import play_valid
from model.game import empty_board, Game
from model.game_state_utils import turn_board
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import *
import pickle

from view.board import Board
from view.board_gui import BoardGui

"""
Playing matches between 2 bots
"""
start = time.time()
file = open('../controller/temp', 'rb')
b = pickle.load(file)
# player1 = Agent('random_player', RandomModel())
player2 = Agent('forward_player',  ForwardModel())
# player3 = Agent('backward_player',  BackwardModel())
# sc1 = play_valid(player1, b, episodes=10)
sc2 = play_valid(player2, b, episodes=2, random_moves=0)
# print(sc1)
print(sc2)
# sc = play_valid(player3, b, episodes=10)
# print(sc)
end = time.time()
log('elapsed seconds :', end - start)

"""
Visualising board
"""
# file = open('board', 'rb')
# board = pickle.load(file)
# # # for x in [(37, 3), (39, 2), (37, 2), (38, 2), (40, 2), (43, 1), (42, 0), (40, 0)]:
# # #     board[x] = 1
# # # boardGUI = BoardGui()
# # # boardGUI.draw_board(board)
# game = Game()
# game.gameState.board = board
# game.gameState.current_position = (10, 3)
# moves = game.gameState.get_full_moves()
# # moves = [frozenset(m[0]) for m in moves]
# # moves = set(moves)
# moves = [m[0] for m in moves]
# print(len(moves))
# for a in moves:
#     print(a)

