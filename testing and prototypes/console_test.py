from multiprocessing.sharedctypes import Value
from random import randrange
import time

Y_SIZE = 0
X_SIZE = 0


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
    for y in range(Y_SIZE):
        for x in range(X_SIZE):
            MATRIX[y][x] = randrange(0,2)

def from_coordinates(cords):
    for coordinate in cords:
        x, y = coordinate[0], coordinate[1]
        MATRIX[y][x] = 1

def build_matrix():
    matrix = []
    for y in range(Y_SIZE):
        row = []
        matrix.append(row)
        for x in range(X_SIZE):
            row.append(0)
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

flag = False
while flag == False:
    try:
        Y_SIZE = int(input('Enter number of rows: (4-256)\n'))
        if Y_SIZE < 4 or Y_SIZE > 256:
            raise ValueError
    except:
        print('Please only use numbers and make sure its within 4-256!')
        Y_SIZE = 0

    if Y_SIZE != 0:
        flag = True
    
flag = False
while flag == False:
    try:
        X_SIZE = int(input('Enter number of columns: (4-256)\n'))
        if X_SIZE < 4 or X_SIZE > 256:
            raise ValueError
    except:
        print('Please only use numbers and make sure its within 4-256!')
        X_SIZE = 0

    if X_SIZE != 0:
        flag = True

MATRIX = build_matrix()
    


'''
Y_SIZE = 16
# at 256x256 gets slow, might get slower on tkinter
X_SIZE = 32
MATRIX = build_matrix()

from_coordinates([[3,3], [3,4], [4,3], [4,4]])
'''
''' Infinite loop with no inputs, for debugging only
while True:
    print('', *readable_matrix(MATRIX), sep = '\n')
    start = time.time()
    MATRIX = tick(MATRIX)
    end = time.time()
    print('tick time: {0:1.7f}s'.format(end-start))
    time.sleep(.1)  # to stop do Ctrl+C in console
'''