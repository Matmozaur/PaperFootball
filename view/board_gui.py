import doctest
import pickle
from _tkinter import TclError
from tkinter import Button
import tkinter as tk
from model.ml_module.dummy_models import RandomModel, ForwardModel, BackwardModel
from view.board import Board
from model.ml_module.agent import Agent
from model.game import Game


def turn_path(path):
    return [([12 - line[0][0], 8 - line[0][1]], [12 - line[1][0], 8 - line[1][1]]) for line in path]


class BoardGui:
    def __init__(self):
        self.root = tk.Tk()
        self.window = tk.Tk()
        self.board = None
        self.agent = None
        self.env = None
        self.agent1 = None
        self.agent2 = None

        # player1_file = open("temp_fw_trained", "rb")
        # player2_file = open("temp_fw_trained", "rb")
        # self.player1 = pickle.load(player1_file)
        # self.player2 = pickle.load(player2_file)


        file = open('../controller/temp_fw_trained', 'rb')
        self.bot = pickle.load(file)
        # self.bot = Agent('dsdas', model=ForwardModel())

        self.set_game_window()

        self.set_panel()

    def get_move(self, bot=None):
        if bot is not None:
            (path, tmp_current_pos, _, board) = bot.get_move(self.env)
        else:
            (path, tmp_current_pos, _, board) = self.agent.get_move(self.env)
        self.env.make_move((path, tmp_current_pos, 0, board))
        self.env.change_player()
        tmp_current_pos = (12 - tmp_current_pos[0], 8 - tmp_current_pos[1])
        path_points = turn_path([self.get_positions(path_el[0], path_el[1]) for path_el in path])
        self.board.implement_move(path_points, tmp_current_pos, self.get_allowable_points())

    def make_move(self):
        self.board.last_move = []
        self.env.change_player()

    def add_line_to_move(self, point):
        # print(point)
        self.env.make_move([[self.env.gameState.get_move(point, self.board.current_point)], point, 0])

        # print(self.env.gameState.get_move((2,6), (1,5)))

        self.board.last_move.append((self.board.current_point, point))
        self.board.implement_move([(self.board.current_point, point)], point, self.get_allowable_points())
        if len(self.get_allowable_points()) == 7:
            self.make_move()

    def get_allowable_points(self):
        return [self.get_positions(line[0], line[1])[1]
                if self.get_positions(line[0], line[1])[0][0] == self.env.gameState.current_position[0] and
                   self.get_positions(line[0], line[1])[0][1] == self.env.gameState.current_position[1]
                else self.get_positions(line[0], line[1])[0]
                for line in self.env.gameState.allowed_actions()]

    def on_click(self, event):
        point = self.board.get_clicked_point(event.x, event.y)
        if point:
            self.add_line_to_move(point)
        if self.env.currentPlayer == -1:
            self.get_move()

    def new_game(self):
        try:
            self.window.destroy()
        except TclError:
            print("Game window closed")
        finally:
            self.window = tk.Tk()
            self.set_game_window()
            self.agent = self.bot
            self.env = Game()
            self.board = Board(self.window)
            self.board.draw_board()
            self.board.color_current_point()
            self.board.color_allowable_points()
            self.board.canvas.pack(fill="both", expand=True)
            # self.board.canvas.bind('<>', self.get_move())
            self.board.canvas.bind('<Button>', self.on_click)

    def set_game_window(self):
        self.window.geometry("400x600")

    def set_panel(self):
        frame = tk.Frame(self.root)
        frame.pack()
        button_new_game = Button(frame, text="New game", command=self.new_game, width="25")
        button_new_robot_fight = Button(frame, text="New robot fight", command=self.new_game_bot, width="25")
        button_next_robot_turn = Button(frame, text="Next move", command=self.next_move_bot, width="25")
        button_quit = Button(frame, text="Quit", command=self.close_windows, width="25")
        button_new_game.pack()
        button_new_robot_fight.pack()
        button_next_robot_turn.pack()
        button_quit.pack()
        self.root.mainloop()

    def new_game_bot(self):
        try:
            self.window.destroy()
        except TclError:
            print("Game window closed")
        finally:
            self.window = tk.Tk()
            self.set_game_window()
            self.agent1 = self.bot
            self.agent2 = self.bot
            self.env = Game()
            self.board = Board(self.window)
            self.board.draw_board()
            self.board.color_current_point()
            self.board.color_allowable_points()
            self.board.canvas.pack(fill="both", expand=True)

    def next_move_bot(self):
        if self.env.currentPlayer == 1:
            self.get_move(self.agent1)
        else:
            self.get_move(self.agent2)


    def close_windows(self):
        self.window.destroy()
        self.root.destroy()

    @staticmethod
    def get_positions(x, y):
        position1 = [0, 0]
        position2 = [0, 0]
        position1[1] = y
        if x % 4 == 0:
            position2[1] = y + 1
            position1[0] = int(x / 4)
            position2[0] = int(x / 4)
        elif x % 4 == 1:
            position2[1] = y
            position1[0] = int(x / 4)
            position2[0] = int(x / 4 + 1)
        elif x % 4 == 2:
            position2[1] = y + 1
            position1[0] = int(x / 4)
            position2[0] = int(x / 4) + 1
        elif x % 4 == 3:
            position2[1] = y + 1
            position1[0] = int(x / 4) + 1
            position2[0] = int(x / 4)
        return position1, position2

    @staticmethod
    def get_all_lines(board):
        lines = []
        for i in range(48):
            for j in range(8):
                if board[i, j] == 1:
                    lines.append(BoardGui.get_positions(i, j))
        return lines


BoardGui()
