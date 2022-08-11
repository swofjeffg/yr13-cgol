from random import randrange
import time

def neighbour_count(x, y):
    return sum(MATRIX[(y+j)%Y_SIZE][(x+i)%X_SIZE] \
        for (i, j) in NEIGHBOURS)

def tick(old_matrix):
    new_matrix = []
    for y in range(Y_SIZE):
        row = []
        for x in range(X_SIZE):
            neighbours = neighbour_count(x, y)
            if old_matrix[y][x] == 1 and (neighbours<2 or neighbours>3):
                row.append(0)
            elif old_matrix[y][x] == 0 and neighbours == 3:
                row.append(1)
            else:
                row.append(old_matrix[y][x])
        new_matrix.append(row)
    return new_matrix

def from_random():
    for y in Y_SIZE:
        for x in range(X_SIZE):
            MATRIX[y][x] = randrange(0,2)

def from_glider():
    coordinates = [[0,1], [1,2], [2,0], [2,1], [2,2]]
    for coordinate in coordinates:
        x, y = coordinate[0], coordinate[1]
        MATRIX[y+10][x] = 1

def build_matrix():
    cell = 0
    matrix = []
    for y in range(Y_SIZE):
        row = []
        matrix.append(row)
        for x in range(X_SIZE):
            row.append(cell)
    return matrix

def readable_matrix(matrix):
    new_matrix = []
    for y in range(Y_SIZE):
        row = ''
        for x in range(X_SIZE):
            if matrix[y][x] == 0:
                row += '-'
            else:
                row += '▢'
        new_matrix.append(row)
    return new_matrix

Y_SIZE = 32
# at 256x256 gets slow, might get slower on tkinter
X_SIZE = 64
MATRIX = build_matrix()
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

from_glider()

while True:
    print('', *readable_matrix(MATRIX), sep = '\n')
    start = time.time()
    MATRIX = tick(MATRIX)
    end = time.time()
    print('tick time: {0:1.7f}s'.format(end-start))
    time.sleep(.1)
