# import numpy as np
# import random
#
# from controller import config
# from model.game import Game
# from model.ml_module.agent import Agent
# from model.ml_module.ml_model import Residual_CNN
# from model.ml_module.user import User


# def playMatchesBetweenVersions(env, run_version, player1version, player2version,
#                                EPISODES, logger, turns_until_tau0, goes_first = 0):
#     if player1version == -1:
#         player1 = User('player1', env.state_size, env.action_size)
#         return 0
#     else:
#         player1_NN = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, env.input_shape,
#                                   env.action_size, config.HIDDEN_CNN_LAYERS)
#         if player1version > 0:
#             player1_network = player1_NN.read(env.name, run_version, player1version)
#             player1_NN.model.set_weights(player1_network.get_weights())
#         player1 = Agent('player1', env.state_size, env.action_size, config.MCTS_SIMS, config.CPUCT, player1_NN)
#     if player2version == -1:
#         player2 = User('player2', env.state_size, env.action_size)
#     else:
#         player2_NN = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, env.input_shape,
#                                   env.action_size, config.HIDDEN_CNN_LAYERS)
#
#         if player2version > 0:
#             player2_network = player2_NN.read(env.name, run_version, player2version)
#             player2_NN.model.set_weights(player2_network.get_weights())
#         player2 = Agent('player2', env.state_size, env.action_size, config.MCTS_SIMS, config.CPUCT, player2_NN)
#
#     scores, memory, points, sp_scores = playMatches(player1, player2, EPISODES, logger, turns_until_tau0, None, goes_first)
#
#     return scores, memory, points, sp_scores
#
#
# def playMatches(player1, player2, EPISODES, logger, turns_until_tau0, memory = None, goes_first = 0):
#     env = Game()
#     scores = {player1.name:0, "drawn": 0, player2.name:0}
#     sp_scores = {'sp':0, "drawn": 0, 'nsp':0}
#     points = {player1.name:[], player2.name:[]}
#     for e in range(EPISODES):
#         state = env.reset()
#         done = 0
#         turn = 0
#         player1.mcts = None
#         player2.mcts = None
#         if goes_first == 0:
#             player1Starts = random.randint(0,1) * 2 - 1
#         else:
#             player1Starts = goes_first
#         if player1Starts == 1:
#             players = {1:{"agent": player1, "name":player1.name}
#                     , -1: {"agent": player2, "name":player2.name}
#                     }
#         else:
#             players = {1:{"agent": player2, "name":player2.name}
#                     , -1: {"agent": player1, "name":player1.name}
#                     }
#         while done == 0:
#             turn = turn + 1
#             #### Run the MCTS algo and return an action
#             if turn < turns_until_tau0:
#                 action, pi, MCTS_value, NN_value = players[state.playerTurn]['agent'].act(state, 1)
#             else:
#                 action, pi, MCTS_value, NN_value = players[state.playerTurn]['agent'].act(state, 0)
#             if memory != None:
#                 ####Commit the move to memory
#                 memory.commit_stmemory(env.identities, state, pi)
#             ### Do the action
#             state, value, done, _ = env.step(action) #the value of the newState from the POV of the new playerTurn i.e. -1 if the previous player played a winning move
#
#             if done == 1:
#                 if memory != None:
#                     #### If the game is finished, assign the values correctly to the game moves
#                     for move in memory.stmemory:
#                         if move['playerTurn'] == state.playerTurn:
#                             move['value'] = value
#                         else:
#                             move['value'] = -value
#                     memory.commit_ltmemory()
#                 if value == 1:
#                     scores[players[state.playerTurn]['name']] = scores[players[state.playerTurn]['name']] + 1
#                     if state.playerTurn == 1:
#                         sp_scores['sp'] = sp_scores['sp'] + 1
#                     else:
#                         sp_scores['nsp'] = sp_scores['nsp'] + 1
#                 elif value == -1:
#                     scores[players[-state.playerTurn]['name']] = scores[players[-state.playerTurn]['name']] + 1
#
#                     if state.playerTurn == 1:
#                         sp_scores['nsp'] = sp_scores['nsp'] + 1
#                     else:
#                         sp_scores['sp'] = sp_scores['sp'] + 1
#                 else:
#                     scores['drawn'] = scores['drawn'] + 1
#                     sp_scores['drawn'] = sp_scores['drawn'] + 1
#                 pts = state.score
#                 points[players[state.playerTurn]['name']].append(pts[0])
#                 points[players[-state.playerTurn]['name']].append(pts[1])
#     return scores, memory, points, sp_scores
import random
import sys
from controller import config
from controller.logger import log
from model.game import Game


def play_training(p1, p2, memory, episodes, random_moves=0):
    """
    plays matches between players and saves results
    @param p1: player 1
    @param p2: player 2
    @param memory: memory object for game state saving
    @param episodes: number of simulated matches
    @param random_moves: number of random moves at the beginning of the match
    """
    env = Game()
    players = {1: p1, -1: p2}
    for e in range(episodes):
        print('game', e)
        # print(sys.getsizeof(memory.ltmemory))
        env.reset()
        done, result = 0, 0
        if random.randint(0, 1) > 0.5:
            p1, p2 = p2, p1
        turn = 0
        while done == 0:
            move = players[env.currentPlayer].get_move(env, turn, random_moves)
            if move is not None:
                if len(move) > 0:
                    # To be changed 1!
                    if len(memory.ltmemory) >= 1.5*config.MEMORY_SIZE:
                        memory.ltmemory.popleft()
                    if turn > 7:
                        memory.append_stmemory(env.currentPlayer, move[3], move[1])
                # memory.append_stmemory(env.currentPlayer, move[3], move[1])
                # print(move[1],'      ',move[0])
            done, result = env.make_move(move)
            if done == 1:
                memory.commit_stmemory(env, result)
            env.change_player()
            turn += 1
    # return memory


def play_valid(p1, p2, episodes, random_moves=0):
    """
    plays matches between players to analyse results
    @param p1: player 1
    @param p2: player 2
    @param episodes: number of games
    @param random_moves: number of random moves at the beginning of the match
    @return: dictionary with games results
    """
    env = Game()
    players = {1: p1, -1: p2}
    scores = {p1.name: 0, p2.name: 0, 'starting_player': 0, 'non-starting_player': 0, }
    for e in range(int(episodes / 2)):
        log('First half, game ',e)
        env.reset()
        env.currentPlayer = 1
        done, result = 0, 0
        turn = 0
        while done == 0:
            move = players[env.currentPlayer].get_move(env, turn, random_moves)
            # print(move[0],'      ',move[1])
            done, result = env.make_move(move)
            # print(env.gameState.board)
            if done == 1:
                scores[players[env.currentPlayer].name] += max(0, result)
                scores[players[-env.currentPlayer].name] += max(0, -result)
            # print('CHANGE PLAYER!!!')
            env.change_player()
            turn += 1
    scores['starting_player'] = scores[p1.name] - scores[p2.name]
    scores['non-starting_player'] = int(episodes / 2) - scores[p1.name] + scores[p2.name]
    for e in range(int(episodes / 2)):
        log('Secound half, game ',e)
        env.reset()
        env.currentPlayer = -1
        done, result = 0, 0
        turn = 0
        while done == 0:
            move = players[env.currentPlayer].get_move(env, turn, random_moves)
            # print(move[0],'      ',move[1])
            done, result = env.make_move(move)
            if done == 1:
                scores[players[env.currentPlayer].name] += max(0, result)
                scores[players[-env.currentPlayer].name] += max(0, -result)
            env.change_player()
            turn += 1
    scores['starting_player'] += scores[p2.name]
    scores['non-starting_player'] += int(episodes / 2) - scores[p2.name]
    return scores
