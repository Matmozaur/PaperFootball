from controller.playing import play_valid
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import *
from model.ml_module.ml_models import DNN, ResidualCNN
import tensorflow as tf
"""
Playing matches between 2 bots
"""

# best_nn = DNN()
# best_nn.model = tf.keras.models.load_model('../resources/DNN_deep_check.h5')
# player1 = Agent('my_player', best_nn)
# player2 = Agent('forward_player',  ForwardModel())
# player3 = Agent('forward_player',  ForwardModel(), search_mode = 'simple')
# sc = play_valid(player1, player2, episodes=4)
# print(sc)

best_nn = ResidualCNN()
best_nn.model = tf.keras.models.load_model('../resources/Residual_CNN_mcts.h5')
player1 = Agent('my_player', best_nn, eval_mode='mcts_boosted')
player2 = Agent('random',  RandomModel(),search_mode='simple')
player3 = Agent('random_mcts',  RandomModel(), eval_mode='mcts_boosted')
sc = play_valid(player1, player2, episodes=4)
print(sc)
sc = play_valid(player1, player3, episodes=4)
print(sc)

