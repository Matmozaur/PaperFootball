import copy

from controller import config
from controller.logger import log_important
from controller.playing import play_training, play_valid
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import RandomModel, ForwardModel
from model.ml_module.memory import Memory
# from model.ml_module.ml_models import Residual_NN_simple
import pickle
import tensorflow as tf
from model.ml_module.ml_models import DNN, ResidualCNN


def main_train(best_player, current_player, memory, iterations):
    i = 0
    while i < iterations:
        i += 1
        log_important('Iteration ', i)
        play_training(best_player, best_player, memory, config.EPISODES, config.TURNS_UNTIL_DET)
        current_player.retrain(memory)
        memory.clear_ltmemory()
        scores = play_valid(current_player, best_player, config.EVAL_EPISODES, random_moves=2)
        log_important(scores)
        if ((scores['current_player'] + 1) / (scores['best_player'] + 1)) > config.SCORING_THRESHOLD:
            best_player.model.model.set_weights(current_player.model.model.get_weights())
            best_player.model.model.save('../resources/Residual_CNN_mcts_trained.h5')

    return best_player


current_nn = ResidualCNN()
best_nn = ResidualCNN()
current_nn.model = tf.keras.models.load_model('../resources/Residual_CNN_mcts.h5')
best_nn.model = tf.keras.models.load_model('../resources/Residual_CNN_mcts.h5')
best_nn.model.set_weights(current_nn.model.get_weights())
memory = Memory(config.MEMORY_SIZE)
current_player = Agent('current_player', current_nn, eval_mode='mcts_boosted')
best_player = Agent('best_player', best_nn, eval_mode='mcts_boosted')

main_train(best_player, current_player, memory, 10)
best_player.model.model.save('../resources/Residual_CNN_mcts_trained.h5')

# memory = Memory(config.MEMORY_SIZE)
# player1 = Agent('mcts_player1', RandomModel(), search_mode='simple', eval_mode='mcts_simple')
# player2 = Agent('mcts_player2', RandomModel(), search_mode='simple', eval_mode='mcts_simple')# print('a')
# play_training(player1, player2, memory, config.EPISODES, config.TURNS_UNTIL_DET)
# file = open('../resources/memory_mcts_1', 'wb')
# pickle.dump(memory, file)
