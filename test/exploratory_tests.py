from controller.playing import play_valid
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import *

"""
Playing matches between 2 bots
"""

player1 = Agent('mcts_player', ForwardModel(), search_mode='simple', eval_mode='mcts_boosted')
player2 = Agent('forward_player',  ForwardModel(), search_mode='simple', eval_mode='model')
sc = play_valid(player1, player2, episodes=2)
print(sc)
