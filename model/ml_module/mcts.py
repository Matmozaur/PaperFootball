import copy
import time
import math
from controller import config
import numpy as np

from model.game import empty_board
from model.game_state import GameState
from model.game_state_utils import turn_board


def get_move_mcts(state):
    mcts=MCTS(Node(state), cpuct=config.MCTS_C)
    return mcts.monte_carlo_tree_search(mcts.root)

class Node:

    def __init__(self, state, parent=None, e=None):
        self.state = state
        self.edges = []
        self.children = []
        self.parent = parent
        self.result = 0
        self.value = 0
        self.visited = 0
        self.e = e

    def isLeaf(self):
        if len(self.children) > 0:
            return False
        else:
            return True

    def simulate(self):
        player = self.state.playerTurn
        const_player = player
        result = 0
        done = False
        # state_copy = copy.deepcopy(self.state)
        i = 1
        while not done:
            move =self.state.get_random_move()
            player = self.state.playerTurn
            done, result =self.state.make_move(move)
            self.state.playerTurn = -self.state.playerTurn
            self.state.board = turn_board(self.state.board)
            self.state.current_position = (12 - self.state.current_position[0], 8 - self.state.current_position[1])

        return const_player * result * player



class Edge:

    def __init__(self, parent, child, move):
        self.parent = parent
        self.child = child
        self.move = move


class MCTS():

    def __init__(self, root, cpuct):
        self.root = root
        self.root.edges = self.root.state.get_full_moves_simple(max_moves=config.MAX_MOVES_MCTS_ROOT, max_time=config.MAX_TIME_MCTS_DEEP)
        self.cpuct = cpuct
        self.T = 0

    def monte_carlo_tree_search(self, root):
        start = time.time()
        while (time.time() - start) <= config.MAX_TIME_MCTS:
            leaf = self.moveToLeaf(root)
            simulation_result, new_node = self.rollout(leaf)
            self.backpropagate(new_node, simulation_result)
            self.T += 1
        print(time.time() - start)
        print(self.best_child(self.root).e[1])
        print(self.T)
        print(self.best_child(self.root).value)
        return self.best_child(self.root).e

    def moveToLeaf(self, currentNode):
        currentNode.visited += 1
        while not currentNode.isLeaf():
            currentNode = self.choose_child(currentNode.children)
            currentNode.visited += 1

        return currentNode

    def rollout(self, node):
        if node.result != 0:
            return node.result, node
        else:
            for e in node.edges:
                node.children.append(self.addNode(node, e))
            currentNode = self.choose_child(node.children)
            currentNode.visited += 1
        return currentNode.simulate(), currentNode



    def choose_child(self, children):
        best_utc = -100
        best_node = None
        for node in children:
            if node.visited == 0:
                return node
            else:
                utc = node.value + self.cpuct * math.sqrt(math.log(self.T)/node.visited)
                if utc > best_utc:
                    best_node = node
                    best_utc = utc
        return best_node

    def backpropagate(self, node, value):
        if node != self.root:
            node.value += value
            node.value /= node.visited
            self.backpropagate(node.parent, -value)

    def addNode(self, parent, edge):
        state = copy.deepcopy(parent.state)
        done, res = state.make_move(edge)

        state.playerTurn = -state.playerTurn
        state.board = turn_board(state.board)
        state.current_position = (12 - state.current_position[0], 8 - state.current_position[1])

        node = Node(state, parent, e=edge)
        if done != 0:
            node.result = res
        # if parent == self.root:
        #     node.edges = node.state.get_full_moves_simple(max_moves=config.MAX_MOVES_MCTS_ROOT,
        #                                                   max_time=config.MAX_TIME_MCTS_DEEP)
        # else:
        #     node.edges = node.state.get_full_moves_simple(max_moves=config.MAX_MOVES_MCTS_DEEP,
        #                                                   max_time=config.MAX_TIME_MCTS_DEEP)
        node.edges = node.state.get_full_moves_simple(max_moves=config.MAX_MOVES_MCTS_DEEP,
                                                          max_time=config.MAX_TIME_MCTS_DEEP)
        if len(node.edges) == 0:
            node.result = -1
        return node

    @staticmethod
    def best_child(root):
        best_value = -100
        best_node = None
        print(root.children)
        for node in root.children:
            if node.value > best_value:
                best_node = node
                best_value = node.value
        return best_node

print(get_move_mcts(GameState(empty_board(), 1, (6, 4))))
