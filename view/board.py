import tkinter as tk
from time import sleep


class Board:
    def __init__(self, window):
        self.window = window
        self.canvas = tk.Canvas(self.window)
        self.square_size = 50
        self.point_radius = 2
        self.points_gui = []
        self.current_point = (6, 4)
        self.last_move = []
        self.allowable_points = [(5, 3), (5, 4), (5, 5), (6, 3), (6, 5), (7, 3), (7, 4), (7, 5)]
        self.clicked_point = (6, 4)
        self.player = 1
        self.lines = []

    # ----------------------------------------squares----------------------------
    def draw_board(self):
        for i in range(3, 5):
            self.canvas.create_rectangle(self.square_size * i, 0, self.square_size * i +

                                         self.square_size, self.square_size, fill='green')
        for i in range(8):
            for j in range(1, 11):
                self.canvas.create_rectangle(self.square_size * i, self.square_size * j,
                                             self.square_size * i + self.square_size,
                                             self.square_size * j + self.square_size, fill='green')
        for i in range(3, 5):
            self.canvas.create_rectangle(self.square_size * i, self.square_size * 11, self.square_size * i +
                                         self.square_size,
                                         self.square_size * 11 + self.square_size, fill='green')

        # ----------------------------------------points saved in table----------------------------

        self.points_gui.append([])
        for j in range(0, 3):
            self.points_gui[0].append(self.canvas.create_oval(self.square_size * j, 0, self.square_size * j,
                                                              0, fill='white', outline=""))

        for j in range(3, 6):
            self.points_gui[0].append(self.canvas.create_oval(self.square_size * j - self.point_radius,
                                                              -self.point_radius, self.square_size * j +
                                                              self.point_radius, self.point_radius, fill='black'))
        for j in range(6, 9):
            self.points_gui[0].append(self.canvas.create_oval(self.square_size * j, 0,
                                                              self.square_size * j, 0, fill='white', outline=""))

        for i in range(1, 12):
            self.points_gui.append([])
            for j in range(0, 9):
                self.points_gui[i].append(self.canvas.create_oval(self.square_size * j - self.point_radius,
                                                                  self.square_size * i - self.point_radius,
                                                                  self.square_size * j + self.point_radius,
                                                                  self.square_size * i + self.point_radius,
                                                                  fill="black"))

        self.points_gui.append([])

        for j in range(0, 3):
            self.points_gui[12].append(self.canvas.create_oval(self.square_size * j, self.square_size * 12,
                                                               self.square_size * j, self.square_size * 12,
                                                               fill="white", outline=""))

        for j in range(3, 6):
            self.points_gui[12].append(self.canvas.create_oval(self.square_size * j - self.point_radius,
                                                               self.square_size * 12 - self.point_radius,
                                                               self.square_size * j + self.point_radius,
                                                               self.square_size * 12 + self.point_radius,
                                                               fill="black"))

        for j in range(6, 9):
            self.points_gui[12].append(self.canvas.create_oval(self.square_size * j, self.square_size * 12,
                                                               self.square_size * j, self.square_size * 12,
                                                               fill="white", outline=""))

    def draw_lines(self, lines):
        for i in range(0, lines.__len__()):
            self.canvas.create_line(50 * lines[i][0][1], 50 * lines[i][0][0], 50 * lines[i][1][1], 50 * lines[i][1][0],
                                    width=2, fill='red')

    def color_allowable_points(self):
        for point in self.allowable_points:
            self.canvas.itemconfig(self.points_gui[point[0]][point[1]], fill="red")

    def color_current_point(self):
        self.points_gui[self.current_point[0]][self.current_point[1]] = \
            self.canvas.create_oval(self.square_size * self.current_point[1] - 5, self.square_size *
                                    self.current_point[0] - 5,
                                    self.square_size * self.current_point[1] + 5, self.square_size *
                                    self.current_point[0] + 5,
                                    fill="blue")

    def uncolor_point(self, point):
        self.canvas.delete(self.points_gui[point[0]][point[1]])
        self.points_gui[point[0]][point[1]] = self.canvas.create_oval(
            self.square_size * point[1] - self.point_radius, self.square_size * point[0] - self.point_radius,
            self.square_size * point[1] + self.point_radius, self.square_size * point[0] +
            self.point_radius, fill="black")

    def get_clicked_point(self, board_x, board_y):
        for point in self.allowable_points:
            if point[0] * 50 - 5 <= board_y <= point[0] * 50 + 5 and point[1] * 50 - 5 <= board_x <= point[1] * 50 + 5:
                return point

    def implement_move(self, path_points, tmp_current_pos, allowable_points):
        self.uncolor_point(self.current_point)
        for allowable_point in self.allowable_points:
            self.uncolor_point(allowable_point)
        for line in path_points:
            self.lines.append(line)
        self.last_move = path_points
        self.draw_lines(path_points)
        self.current_point = tmp_current_pos
        self.allowable_points = allowable_points
        self.color_allowable_points()
        self.color_current_point()