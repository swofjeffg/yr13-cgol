from tkinter import *
from random import randrange
import time

ROOT = Tk()
MASTER = Frame(ROOT)
MASTER.place(relx=.5, rely=.5, anchor=CENTER)

X_SIZE, Y_SIZE = 16, 16
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
            MATRIX[y][x] = randrange(0,2)

def neighbour_count(x, y):
    return sum(MATRIX[(y+j)%Y_SIZE][(x+i)%X_SIZE] \
        for (i, j) in NEIGHBOURS)

def display_grid():
    for y in range(Y_SIZE):
        for x in range(X_SIZE):
            if MATRIX[x][y] == 1:
                Label(MASTER, bg='#00ff00', width=2, height=1).grid(column=x, row=y)
            else:
                Label(MASTER, bg='#000000', width=2, height=1).grid(column=x, row=y)


MATRIX = build_matrix()
from_random()
display_grid()


ROOT.update()
ROOT.minsize(ROOT.winfo_width(), ROOT.winfo_height())
ROOT.mainloop()