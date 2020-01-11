import doctest
import pickle
import webbrowser
from _tkinter import TclError
from tkinter import Button, BOTTOM, BOTH
import tkinter as tk
from model.ml_module.dummy_models import RandomModel, ForwardModel, BackwardModel
from view.board import Board
from model.ml_module.agent import Agent
from model.game import Game

LARGE_FONT = ("Verdana", 12)


def turn_path(path):
    return [([12 - line[0][0], 8 - line[0][1]], [12 - line[1][0], 8 - line[1][1]]) for line in path]


class BoardGui:
    def __init__(self):
        self.root = None
        self.window = None
        self.board = None
        self.agent = None
        self.env = None
        self.agent1 = None
        self.agent2 = None
        self.bot = None
        self.player1 = None
        self.player2 = None

    def start(self):
        player1_file = open("temp_fw_trained", "rb")
        player2_file = open("temp_fw_trained", "rb")
        self.player1 = pickle.load(player1_file)
        self.player2 = pickle.load(player2_file)

        self.root = tk.Tk()
        file = open('../controller/temp_fw_trained', 'rb')
        self.bot = pickle.load(file)
        # self.bot = Agent('dsdas', model=ForwardModel())

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

    def next_move_bot(self):
        if self.env.currentPlayer == 1:
            self.get_move(self.agent1)
        else:
            self.get_move(self.agent2)

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

    def draw_board(self, board):
        lines = self.get_all_lines(board)
        self.set_game_window()
        self.agent = self.bot
        self.env = Game()
        self.board = Board(self.window)
        self.board.draw_board()
        self.board.color_current_point()
        self.board.color_allowable_points()
        self.board.canvas.pack(fill="both", expand=True)
        self.board.draw_lines(lines)
        self.window.mainloop()

    def test_board(self):
        self.window = tk.Tk()
        self.set_game_window()
        self.env = Game()
        self.board = Board(self.window)
        self.board.draw_board()
        self.board.color_current_point()
        self.board.color_allowable_points()
        self.board.canvas.pack(fill="both", expand=True)
        self.env.gameState.board[17, 3] = 1
        self.env.gameState.board[20, 3] = 1
        self.env.gameState.board[21, 4] = 1
        self.env.gameState.current_position = (4, 3)
        # print([self.env.gameState.get_move(x,y) for x,y in [[(4,3),(5,3)],[(5,3),(5,4)],[(5,4),(6,4)]]])
        print(self.env.gameState.get_move((6, 4), (5, 4)))
        # print(self.env.gameState.get_full_moves())
        self.board.draw_lines([self.get_positions(x, y) for x, y in [(21, 4), (20, 3)]])
        # self.board.draw_lines([[(4,3),(5,3)],[(5,3),(5,4)],[(5,4),(6,4)]])
        self.window.mainloop()


class GameWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(fill=BOTH, expand=True)

        self.geometry("400x700")
        self.frames = {}

        for F in (Menu, NewGameBU, BBMenu, NewGameBB):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Paper Football", font=LARGE_FONT)
        label.pack()

        button_new_game = tk.Button(self, text="New Game user-bot",
                                    command=lambda: controller.show_frame(NewGameBU), width="25")
        button_new_game.pack()

        button_new_bot_game = tk.Button(self, text="New Game bot-bot",
                                        command=lambda: controller.show_frame(BBMenu), width="25")
        button_new_bot_game.pack()

        button_instructions = tk.Label(self, text="How To Play", fg="blue", cursor="hand2", width="25")
        button_instructions.pack()
        button_instructions.bind("<Button-1>", lambda e: webbrowser.open_new("https://en.wikipedia.org/wiki/Paper_soccer"))

        button_instructions.pack()

        button_quit = tk.Button(self, text="Quit",
                                command=self.destroy, width="25")
        button_quit.pack()


class NewGameBU(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.boardGui = BoardGui()
        self.boardGui.file = open('../controller/temp_fw_trained', 'rb')
        self.boardGui.bot = pickle.load(self.boardGui.file)
        self.boardGui.agent = self.boardGui.bot
        self.boardGui.env = Game()
        self.boardGui.board = Board(self)
        self.boardGui.board.draw_board()
        self.boardGui.board.color_current_point()
        self.boardGui.board.color_allowable_points()
        self.boardGui.board.canvas.config(width=400, height=600)
        self.boardGui.board.canvas.bind('<Button>', self.boardGui.on_click)
        self.boardGui.board.canvas.pack(fill = BOTH, expand = True)
        button1 = tk.Button(self, text="Restart Game",
                            command=lambda: controller.show_frame(NewGameBU))
        button1.pack(side=BOTTOM)

        button2 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(Menu))
        button2.pack(side=BOTTOM)


class NewGameBB(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Menu))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(NewGameBU))
        button2.pack()


class BBMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="Player 1", font=LARGE_FONT)
        label1.pack(pady=10, padx=10)
        variable1 = tk.StringVar(self)
        variable1.set("Random")
        p1 = tk.OptionMenu(self, variable1, "Random", "Forward", "Intelligent")
        p1.pack()
        label2 = tk.Label(self, text="Player 2", font=LARGE_FONT)
        label2.pack(pady=10, padx=10)
        variable2 = tk.StringVar(self)
        variable2.set("Random")
        p2 = tk.OptionMenu(self, variable2, "Random", "Forward", "Intelligent")
        p2.pack()
        button_play = tk.Button(self, text="Play",
                            command=lambda: controller.show_frame(NewGameBB))
        button_play.pack()


app = GameWindow()
app.mainloop()