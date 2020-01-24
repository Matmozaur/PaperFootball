import copy

from controller import config
from controller.playing import play_training, play_valid
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import RandomModel, ForwardModel
from model.ml_module.memory import Memory
# from model.ml_module.ml_models import Residual_NN_simple
import pickle


# def main_train():
#     current_nn = Residual_NN_simple(config.REG_CONST, config.LEARNING_RATE, config.INPUT_SHAPE, config.HIDDEN_CNN_LAYERS)
#     best_nn = Residual_NN_simple(config.REG_CONST, config.LEARNING_RATE, config.INPUT_SHAPE, config.HIDDEN_CNN_LAYERS)
#     best_nn.model.set_weights(current_nn.model.get_weights())
#     memory = Memory(config.MEMORY_SIZE)
#     current_player = Agent('current_player', current_nn)
#     best_player = Agent('best_player',  best_nn)
#     # print('a')
#     i = 0
#     while i < 120:
#         i+=1
#         print('Iteration ',i)
#         play_training(best_player, best_player, memory, config.EPISODES, config.TURNS_UNTIL_DET)
#         if len(memory.ltmemory) >= config.MEMORY_SIZE:
#             current_player.retrain(memory)
#             # memory_random_1.clear_ltmemory()
#             scores = play_valid(current_player, best_player, config.EVAL_EPISODES, random_moves=2)
#             print(scores)
#             if ((scores['current_player']+1)/(scores['best_player']+1)) > config.SCORING_THRESHOLD:
#                 best_player.model.model.set_weights(current_player.model.model.get_weights())
#                 file = open('temp', 'wb')
#                 pickle.dump(best_player, file)
#
#     return best_player



memory = Memory(config.MEMORY_SIZE)
player1 = Agent('mcts_player1', RandomModel(), search_mode='simple', eval_mode='mcts_simple')
player2 = Agent('mcts_player2', RandomModel(), search_mode='simple', eval_mode='mcts_simple')# print('a')
play_training(player1, player2, memory, config.EPISODES, config.TURNS_UNTIL_DET)
file = open('../resources/memory_mcts_1', 'wb')
pickle.dump(memory, file)






