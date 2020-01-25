from controller.playing import play_valid
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import *
from model.ml_module.ml_models import DNN
import tensorflow as tf
"""
Playing matches between 2 bots
"""

# player1 = Agent('mcts_player', ForwardModel(), search_mode='simple', eval_mode='mcts_boosted')
# player2 = Agent('forward_player',  ForwardModel(), search_mode='simple', eval_mode='model')
# sc = play_valid(player1, player2, episodes=2)
# print(sc)
best_nn = DNN()
best_nn.model = tf.keras.models.load_model('../resources/DNN_deep_check.h5')
player1 = Agent('my_player', best_nn)
player2 = Agent('forward_player',  ForwardModel())
player3 = Agent('forward_player',  ForwardModel(), search_mode = 'simple')
sc = play_valid(player1, player3, episodes=4)
print(sc)
