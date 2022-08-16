from tkinter import *
from random import randrange
import time

ROOT = Tk()

X_SIZE, Y_SIZE = 256, 256 # how many columns and rows
SCALE = 2   # how big is the whole canvas

CANVAS = Canvas(ROOT, height=SCALE*X_SIZE, width=SCALE*Y_SIZE)
CANVAS.place(relx=.5, rely=.5, anchor=CENTER)

NEIGHBOURS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

class App():
    def __init__(self, root):
        self.data_matrix = self.build_matrix()
        self.root = root
        self.from_random()
        self.display_matrix = self.display_grid()

    def build_matrix(self):
        matrix = []
        for _ in range(Y_SIZE):
            row = []
            matrix.append(row)
            for _ in range(X_SIZE):
                row.append(0)
        return matrix

    def from_random(self):
        for y in range(Y_SIZE):
            for x in range(X_SIZE):
                self.data_matrix[y][x] = randrange(0,2)

    def neighbour_count(self, x, y):
        return sum(self.data_matrix[(y+j)%Y_SIZE][(x+i)%X_SIZE] \
            for (i, j) in NEIGHBOURS)

    def display_grid(self):
        matrix = []
        for y in range(Y_SIZE):
            row = []
            for x in range(X_SIZE):
                top_left_x = x * SCALE  # create 4 points in which the rectangle sits in
                bottom_right_x = x * SCALE + SCALE
                top_left_y = y * SCALE
                bottom_right_y = y * SCALE + SCALE
                if self.data_matrix[x][y] == 1:
                    row.append(CANVAS.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill='#00ff00', width=0))
                else:
                    row.append(CANVAS.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill='#aaaaaa', width=0))
            matrix.append(row)
        return matrix
    
    def configure_grid(self):
        id = 0
        for y in range(Y_SIZE):
            for x in range(X_SIZE):
                id += 1
                if self.data_matrix[x][y] == 1:
                    CANVAS.itemconfigure(id, fill='#00ff00')
                else:
                    CANVAS.itemconfigure(id, fill='#000000')

    def tick(self, old_matrix):
        new_matrix = []
        for y in range(Y_SIZE):
            row = []
            for x in range(X_SIZE):
                neighbours = self.neighbour_count(x, y)
                if old_matrix[y][x] == 1 and (neighbours<2 or neighbours>3):
                    row.append(0)
                elif old_matrix[y][x] == 0 and neighbours == 3:
                    row.append(1)
                else:
                    row.append(old_matrix[y][x])
            new_matrix.append(row)
        return new_matrix
    
    def controller(self):
        start = time.time()
        self.data_matrix = self.tick(self.data_matrix)
        self.configure_grid()
        end = time.time()
        print('tick time: {0:1.7f}s'.format(end-start))
        self.root.after(1, self.controller)

if __name__ == '__main__':
    ROOT.update()
    ROOT.minsize(ROOT.winfo_width(), ROOT.winfo_height())
    app = App(ROOT)
    app.controller()
    ROOT.mainloop()