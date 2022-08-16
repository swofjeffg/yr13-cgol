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

def build_matrix():
    matrix = []
    for _ in range(Y_SIZE):
        row = []
        matrix.append(row)
        for _ in range(X_SIZE):
            row.append(0)
    return matrix

def from_random():
    for y in range(Y_SIZE):
        for x in range(X_SIZE):
            DATA_MATRIX[y][x] = randrange(0,2)

def neighbour_count(x, y):
    return sum(DATA_MATRIX[(y+j)%Y_SIZE][(x+i)%X_SIZE] \
        for (i, j) in NEIGHBOURS)

def display_grid():
    matrix = []
    for y in range(Y_SIZE):
        row = []
        for x in range(X_SIZE):
            top_left_x = x * SCALE  # create 4 points in which the rectangle sits in
            bottom_right_x = x * SCALE + SCALE
            top_left_y = y * SCALE
            bottom_right_y = y * SCALE + SCALE
            if DATA_MATRIX[x][y] == 1:
                row.append(CANVAS.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill='#00ff00', width=0))
            else:
                row.append(CANVAS.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill='#000000', width=0))
        matrix.append(row)
    return matrix


DATA_MATRIX = build_matrix()
DISPLAY_MATRIX = display_grid()
from_random()
display_grid()


ROOT.update()
ROOT.minsize(ROOT.winfo_width(), ROOT.winfo_height())
ROOT.mainloop()