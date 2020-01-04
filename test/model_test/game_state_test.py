import unittest
import numpy as np

from model.game import Game


class GameStateTest(unittest.TestCase):

    def test_turn_empty_board(self):
        game = Game()
        board = game.gameState.turn_board(game.gameState.board)
        self.assertEqual(game.gameState.board.tolist(), board.tolist())
        board[0, 0] = 0
        self.assertNotEqual(game.gameState.board.tolist(), board.tolist())

    def test_turn_full_board(self):
        game = Game()
        board = np.zeros((48, 8), dtype=int)
        board[:48, :8] = 1
        # print(board)
        self.assertEqual(game.gameState.turn_board(board).tolist(), board.tolist())

    def test_turn_board_with_lines(self):
        game = Game()
        board = game.gameState.board.copy()
        game.gameState.board[18, 5] = 1
        game.gameState.board[28, 6] = 1
        board[30, 2] = 1
        board[20, 1] = 1
        self.assertEqual(game.gameState.turn_board(game.gameState.board).tolist(), board.tolist())

    def test_turn_board_with_broad_lines(self):
        game = Game()
        board = game.gameState.board.copy()
        game.gameState.board[4, 0] = 1
        game.gameState.board[42, 0] = 1
        game.gameState.board[6, 7] = 1
        board[44, 7] = 1
        board[6, 7] = 1
        board[42, 0] = 1

        self.assertEqual(game.gameState.turn_board(game.gameState.board).tolist(), board.tolist())

    def test_get_neighbours_start(self):
        game = Game()
        neighbours = {(5, 3), (5, 4), (5, 5), (6, 3), (6, 5), (7, 3), (7, 4), (7, 5)}

        self.assertEqual(set(game.gameState.get_neighbours((6, 4))), neighbours)

    def test_get_neighbours_my_gate(self):
        game = Game()
        neighbours = {(10, 2), (10, 3), (10, 4), (11, 2), (11, 4), (12, 2), (12, 3), (12, 4)}
        self.assertEqual(set(game.gameState.get_neighbours((11, 3))), neighbours)

    def test_get_move_vertical(self):
        game = Game()
        line = (41, 3)
        self.assertEqual(game.gameState.get_move((10, 3), (11, 3)), line)

    def test_get_move_horizontal(self):
        game = Game()
        line = (44, 3)
        self.assertEqual(game.gameState.get_move((11, 3), (11, 4)), line)

    def test_get_move_slope(self):
        game = Game()
        line = (43, 3)
        self.assertEqual(game.gameState.get_move((11, 3), (10, 4)), line)

    def test_get_positions(self):
        game = Game()
        positions = ((11, 3), (10, 4))
        self.assertEqual(game.gameState.get_positions(43, 3), positions)

    def test_allowed_actions_start(self):
        game = Game()
        allowed = {(24, 3), (24, 4), (21, 4), (25, 4), (22, 3), (27, 3), (26, 4), (23, 4)}
        self.assertEqual(set(game.gameState.allowed_actions()), allowed)

    def test_allowed_actions_after_by_corner(self):
        game = Game()
        board = game.gameState.board.copy()
        board[26, 4] = 1
        board[30, 5] = 1
        board[33, 6] = 1
        board[38, 6] = 1
        board[37, 7] = 1
        board[36, 7] = 1
        allowed = {(39, 7), (34, 7)}
        self.assertEqual(set(game.gameState.allowed_actions(board, (9, 8))), allowed)

