import copy
import time
import math
from controller import config
import numpy as np

from model.game import empty_board
from model.game_state import GameState
from model.game_state_utils import turn_board


def get_move_mcts(state, model=None):
    mcts=MCTS(Node(state), cpuct=config.MCTS_C)
    if mcts.root is None:
        return state.get_random_move()
    return mcts.monte_carlo_tree_search(mcts.root, model)

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
        if parent is None:
            self.level = 0
        else:
            self.level = parent.level + 1

    def isLeaf(self):
        if len(self.children) > 0:
            return False
        else:
            return True

    def simulate(self):
        # print('level',self.level)
        # print('visited',self.visited)
        player = self.state.playerTurn
        const_player = player
        result = 0
        done = False
        # state_copy = copy.deepcopy(self.state)
        i = 1
        while not done:
            move =self.state.get_random_move()
            # if len(move) > 0:
            #     print(move[1])
            # else:
                # print('none')
            player = self.state.playerTurn
            # print(player)
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
        # for e in self.root.edges:
        #     print(e[1])
        if len(self.root.edges) == 0:
            self.root = None
        self.cpuct = cpuct
        self.T = 1

    def monte_carlo_tree_search(self, root, model=None):
        start = time.time()
        while (time.time() - start) <= config.MAX_TIME_MCTS:
        # while self.T<2:
            leaf = self.moveToLeaf(root)
            if model is None:
                simulation_result, new_node = self.rollout(leaf)
            else:
                simulation_result, new_node = self.rollout_boosted(leaf, model)
            # print('lvl',new_node.level)
            # print('res',simulation_result)
            self.backpropagate(new_node, simulation_result)
            self.T += 1
        # print(time.time() - start)
        # print(self.best_child(self.root).e[1])
        # print(self.T)
        # # self.print_structure()
        # print('value', self.best_child(self.root).value)
        return self.best_child(self.root).e


    def moveToLeaf(self, currentNode):
        currentNode.visited += 1
        while not currentNode.isLeaf():
            currentNode = self.choose_child(currentNode.children)
            currentNode.visited += 1
        # print('leaf',currentNode.level)

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

    def rollout_boosted(self, node, model):
        if node.result != 0:
            return node.result, node
        else:
            for e in node.edges:
                node.children.append(self.addNode_boosted(node, e, model))
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
            node.value = ((node.visited - 1) * node.value - value) /node.visited
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
            node.value = 999999*res
        node.edges = node.state.get_full_moves_simple(max_moves=config.MAX_MOVES_MCTS_DEEP,
                                                          max_time=config.MAX_TIME_MCTS_DEEP)
        if len(node.edges) == 0:
            node.result = -1
        return node

    def addNode_boosted(self, parent, edge, model):
        state = copy.deepcopy(parent.state)
        done, res = state.make_move(edge)
        val = model.predict(state.board, state.current_position)

        state.playerTurn = -state.playerTurn
        state.board = turn_board(state.board)
        state.current_position = (12 - state.current_position[0], 8 - state.current_position[1])

        node = Node(state, parent, e=edge)
        if done != 0:
            node.result = res
            node.value = 999999*res
        else:
            node.value = val
            node.visited = 1
        node.edges = node.state.get_full_moves_simple(max_moves=config.MAX_MOVES_MCTS_DEEP,
                                                          max_time=config.MAX_TIME_MCTS_DEEP)
        if len(node.edges) == 0:
            node.result = -1
        return node

    @staticmethod
    def best_child(root):
        best_value = -100
        best_node = None
        # print(len(root.children))
        for node in root.children:
            if node.value > best_value:
                best_node = node
                best_value = node.value
        return best_node

    def print_structure(self):
        print('root',self.root)
        for c in self.root.children:
            print(c.value)


# board = empty_board()
# print(get_move_mcts(GameState(board, 1, (2, 4))))
