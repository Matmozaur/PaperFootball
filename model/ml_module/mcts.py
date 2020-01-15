import copy
import time
import math
from controller import config
import numpy as np


class Node:

    def __init__(self, state, parent=None):
        self.state = state
        self.edges = []
        self.children = []
        self.parent = parent
        self.result = 0
        self.value = 0
        self.visited = 0

    def isLeaf(self):
        if len(self.children) > 0:
            return False
        else:
            return True

    def simulate(self):
        global result, player
        done = False
        state_copy = copy.deepcopy(self.state)
        while not done:
            move =state_copy.get_random_move()
            player = state_copy.playerTurn
            done, result =state_copy.make_move(move)
        return self.state.playerTurn * result * player



class Edge:

    def __init__(self, parent, child, move):
        self.parent = parent
        self.child = child
        self.move = move


class MCTS():

    def __init__(self, root, cpuct):
        self.root = root
        self.cpuct = cpuct
        self.T = 0

    def monte_carlo_tree_search(self, root):
        start = time.time()
        while (time.time() - start) <= config.MAX_TIME_MCTS:
            leaf = self.moveToLeaf(root)
            simulation_result, new_node = self.rollout(leaf)
            self.backpropagate(new_node, simulation_result)
            self.T += 1

        return self.best_child(root)

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
        best_utc = 0
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
            node.value += value/node.visited
            self.backpropagate(node.parent, -value)

    def addNode(self, parent, edge):
        state = parent.state
        done, res = state.make_move(edge)
        node = Node(state, parent)
        if done != 0:
            node.result = res
        if parent == self.root:
            node.edges = node.state.get_full_moves_simple(self, max_moves=config.MAX_MOVES_MCTS_ROOT,
                                                          max_time=config.MAX_TIME_MCTS_DEEP)
        else:
            node.edges = node.state.get_full_moves_simple(self, max_moves=config.MAX_MOVES_MCTS_DEEP,
                                                          max_time=config.MAX_TIME_MCTS_DEEP)
        return node

    @staticmethod
    def best_child(root):
        best_value = 0
        best_node = None
        for node in root.children:
            if node.value > best_value:
                best_node = node
                best_value = node.value
        return best_node
