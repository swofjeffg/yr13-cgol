from tkinter import *
from random import randrange
import time
import math

'''
"Desired width" is the width of the program itself, and
columns/rows refers to the number of columns/rows.
'''

DESIRED_WIDTH = 1000
COLUMNS, ROWS = int(round(192/2)), int(round(128/2))


ROOT = Tk()
SCALE = int(round(DESIRED_WIDTH/COLUMNS))   # rounding the scale ensures all cubes are perfectly sized and not squeezed/squished
master = Frame(ROOT, bg='#111011')
CANVAS = Canvas(master, width=SCALE*COLUMNS, height=SCALE*ROWS, bg='#111011', highlightbackground='#111011')
CANVAS.pack()
master.place(relx=.5, rely=.5, anchor=CENTER)

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

class App:
    def __init__(self, root):
        self.root = root
        self.display_matrix = self.display_grid()
        self.from_random()
        self.id = -1
        CANVAS.bind('<Button-1>', self.canvas_click)
        CANVAS.bind('<B1-Motion>', self.canvas_click)
        self.play = True

        self.button = Button(self.root, text='Pause', command=self.button_press)
        self.button.pack()
    
    def button_press(self):
        if self.play == True:
            self.play = False
            self.button.configure(text='Play')
        else:
            self.play = True
            self.button.configure(text='Pause')
    
    def canvas_click(self, event):
        clicked_box = ((math.ceil(event.x/SCALE)), math.ceil((event.y/SCALE)))
        id = ((clicked_box[1]-1)*COLUMNS) + clicked_box[0]
        if self.display_matrix[clicked_box[1]-1][clicked_box[0]-1] == 0 and self.id != id:
            CANVAS.itemconfigure(id, fill='#099B4F')
            self.display_matrix[clicked_box[1]-1][clicked_box[0]-1] = 1
        elif self.display_matrix[clicked_box[1]-1][clicked_box[0]-1] == 1 and self.id != id:
            CANVAS.itemconfigure(id, fill='#111111')
            self.display_matrix[clicked_box[1]-1][clicked_box[0]-1] = 0
        
        self.id = id
        
        

    def from_random(self):
        for y in range(ROWS):
            for x in range(COLUMNS):
                self.display_matrix[y][x] = randrange(0,1)

    def neighbour_count(self, x, y):
        return sum(self.display_matrix[(y+j)%ROWS][(x+i)%COLUMNS] for (i, j) in NEIGHBOURS)

    def display_grid(self):
        matrix = []
        for y in range(ROWS):
            row = []
            for x in range(COLUMNS):
                top_left_x = x * SCALE  # create 4 points in which the rectangle sits in
                bottom_right_x = x * SCALE + SCALE
                top_left_y = y * SCALE
                bottom_right_y = y * SCALE + SCALE
                row.append(0)
                CANVAS.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill='#363636', width=1, outline='#111011')
            matrix.append(row)
        return matrix
    
    def display_tick(self, old_matrix):
        new_matrix = []
        id = 0
        for y in range(ROWS):
            row = []
            for x in range(COLUMNS):
                id += 1
                neighbours = self.neighbour_count(x, y)
                if old_matrix[y][x] == 1 and (neighbours<2 or neighbours>3):
                    CANVAS.itemconfigure(id, fill='#141314')
                    row.append(0)
                elif old_matrix[y][x] == 0 and neighbours == 3:
                    CANVAS.itemconfigure(id, fill='#099B4F')
                    row.append(1)
                else:
                    row.append(old_matrix[y][x])
            new_matrix.append(row)
        return new_matrix
    
    def controller(self):
        if self.play == True:
            start = time.time()
            self.display_matrix = self.display_tick(self.display_matrix)
            end = time.time()
            #print('tick time: {0:1.7f}s'.format(end-start))
        self.root.after(1, self.controller)

if __name__ == '__main__':
    ROOT.update()
    ROOT.minsize(ROOT.winfo_width(), ROOT.winfo_height())
    ROOT.minsize(int(round(COLUMNS*SCALE)),int(round(ROWS*SCALE)))
    ROOT.config(bg='#111011')
    app = App(ROOT)
    app.controller()
    ROOT.mainloop()