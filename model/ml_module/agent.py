
import copy
import random
import time

from controller import config
import numpy as np

from controller.logger import log
from model.ml_module.mcts import get_move_mcts


class Agent:
    def __init__(self, name, model, search_mode='deep', eval_mode='model'):
        self.name = name
        self.model = model
        self.search_mode = search_mode
        self.eval_mode = eval_mode

    def retrain(self, memory, config=config):
        """
        retrain model basing on played games
        """
        for i in range(config.TRAINING_LOOPS):
            training_states = np.array([self.model.convert_to_model_input(row['state'], row['current_position']) for row in memory.ltmemory])
            training_targets = np.array([row['result'] for row in memory.ltmemory])
            training_targets = training_targets > 0
            training_targets = training_targets.astype(int)
            log(training_states.shape)
            self.model.fit(training_states, training_targets, epochs=config.EPOCHS, verbose=1, batch_size=config.BATCH_SIZE,
                           shuffle=config.SHUFFLE, validation_split=config.VALIDATION_SPLIT)

    def get_move(self, env, turn=1, random_moves=0):
        if self.eval_mode == 'model':
            return self.get_move_model(env, turn=1, random_moves=0)
        if self.eval_mode == 'mcts_simple':
            return self.get_move_mcts_simple(env, turn=1, random_moves=0)
        if self.eval_mode == 'mcts_boosted':
            return self.get_move_mcts_boosted(env, turn=1, random_moves=0)

    def get_move_model(self, env, turn=1, random_moves=0):
        """
        @param env: current game state
        @param turn: flag
        @param random_moves: number of moves before agent starts to play deterministic
        @return:
        """
        best_move, best_score = None, -100
        all_moves = env.get_all_allowed_moves(type=self.search_mode)
        start = time.time()
        for move in all_moves:
            sc = self.score_move(move, env, turn, random_moves)
            # print(sc)
            if move[2] == 1:
                return move
            if sc > best_score:
                best_score = sc
                best_move = move
                # if sc == 100:
                #     return best_move
        end = time.time()
        log('elapsed seconds evaluating:', end - start)
        log('score', best_score)
        return best_move

    def get_move_mcts_simple(self, env, turn=1, random_moves=0):
        """
        @param env: current game state
        @param turn: flag
        @param random_moves: number of moves before agent starts to play deterministic
        @return:
        """
        return get_move_mcts(copy.deepcopy(env.gameState))

    def get_move_mcts_boosted(self, env, turn=1, random_moves=0):
        """
        @param env: current game state
        @param turn: flag
        @param random_moves: number of moves before agent starts to play deterministic
        @return:
        """
        return get_move_mcts(copy.deepcopy(env.gameState), self.model)



    def score_move(self, move, env, turn, random_moves):
        """
        @param move: proposed move
        @param env: current game state
        @param turn: flag
        @param random_moves: configuration parametr
        @return: score of the move
        """
        env_test = copy.deepcopy(env)
        done, result = env_test.make_move(move)
        if done == 1:
            if result == 1:
                return 100
            else:
                return -99
        else:
            if turn < random_moves:
                return random.uniform(0, 1)
            return self.model.predict(env_test.gameState.board, env_test.gameState.current_position)
