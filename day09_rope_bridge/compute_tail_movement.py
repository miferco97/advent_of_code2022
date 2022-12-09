import os
import sys
import copy
import math
from typing import List, Tuple, Dict
from collections import deque


class SnakeParts():
    def __init__(self, i_initial, j_initial):
        self.i = i_initial
        self.j = j_initial
        self.last_i = i_initial
        self.last_j = j_initial
        self.last_move_i = 0
        self.last_move_j = 0

    def last_move_was_diag(self):
        return (self.i != self.last_i) and (self.j != self.last_j)

    def follow(self, other, is_head):
        diff_i = float(other.i - self.i)
        diff_j = float(other.j - self.j)
        dist = math.sqrt(math.pow(diff_i, 2) + math.pow(diff_j, 2))
        if dist > 2:
            # move in diag
            movement = int(diff_i/abs(diff_i)), int(diff_j/abs(diff_j))
            self.move(*movement)
        elif dist == 2:
            di = int(diff_i/abs(diff_i)) if int(diff_i) else 0
            dj = int(diff_j/abs(diff_j)) if int(diff_j) else 0
            self.move(di, dj)

    def move_at(self, i, j):
        self.last_i, self.last_j = (self.i, self.j)
        self.i, self.j = (i, j)
        self.last_move_i = (self.i - self.last_i)
        self.last_move_j = (self.j - self.last_j)

    def move(self, i, j):
        res_i = self.i + i
        res_j = self.j + j
        self.move_at(res_i, res_j)

    def get_position(self):
        return (self.i, self.j)

    def __repr__(self) -> str:
        return f'[{self.i}, {self.j}]'


class Snake():
    def __init__(self, n_parts, initial_i, initial_j):
        self.body: List[SnakeParts] = []
        for i in range(n_parts):
            self.body.append(SnakeParts(initial_i, initial_j))
        print(len(self.body))

    def move_head(self, dir: str):
        directions = {'U': (-1, 0),
                      'D': (1, 0),
                      'R': (0, 1),
                      'L': (0, -1)}

        self.body[0].move(directions[dir][0], directions[dir][1])
        for i in range(1, len(self.body)):
            self.body[i].follow(self.body[i-1], bool(i-1 == 0))
        # print(self.body)

    def head_position(self):
        return self.body[0].get_position()

    def tail_position(self):
        return self.body[-1].get_position()


class Matrix():
    def __init__(self, data, n_rows, n_cols, snake_size=2, start=None):
        self.n_rows = int(n_rows)
        self.n_cols = int(n_cols)
        self.col_lims = [0, self.n_cols-1]
        self.row_lims = [0, self.n_rows-1]
        if start is None:
            self.start = (self.n_rows//2, self.n_cols//2)
        else:
            self.start = start
        # self.start = (self.n_rows-1, 0)
        print('SNAKE_SIZE: ', snake_size)
        self.snake = Snake(snake_size, self.start[0], self.start[1])

        if data is not None:
            self.data = data
        else:
            self.data = ['.'] * (self.n_rows * self.n_cols)

    def __call__(self, i: int, j: int):
        return self.data[(i*self.n_cols)+j]

    def col(self, j) -> List[int]:
        col = []
        for i in range(self.n_rows):
            col.append(self.__call__(i, j))
        return col

    def row(self, i) -> List[int]:
        row = []
        for j in range(self.n_cols):
            row.append(self.__call__(i, j))
        return row

    def __repr__(self) -> str:
        repr = ''
        for i in range(self.n_rows):
            items = []
            for j in range(self.n_cols):
                snake_printed = False
                for k in range(len(self.snake.body)):
                    sn_i, sn_j = self.snake.body[k].get_position()
                    if (i == sn_i and j == sn_j) and not snake_printed:
                        if k == 0:
                            items.append('H')
                        else:
                            items.append(str(k))
                        snake_printed = True
                if snake_printed:
                    continue
                elif i == self.start[0] and j == self.start[1]:
                    items.append('s')
                else:
                    items.append(self(i, j))
                    # items.append('.')
            repr += ' '.join(items)
            repr += '\n'
        return repr[:-1]

    def moveHead(self, direction: str) -> None:
        self.snake.move_head(direction)
        i, j = self.snake.tail_position()
        self.data[(i*self.n_cols)+j] = '#'
        # print(self.snake.head_position())

    def count_caracters(self, char: str = '#') -> int:
        n_chars = 0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self(i, j) == char:
                    n_chars += 1
                elif i == self.start[0] and j == self.start[1]:
                    n_chars += 1
        return n_chars


def parse_head_instructions(filename: str) -> List[str]:
    instructions = []

    with open(filename, 'r') as f:
        for line in f.readlines():
            movement, quantity = line.strip().split(' ')
            instruction = [movement] * int(quantity)
            instructions.extend(instruction)
    return instructions


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    instuctions = parse_head_instructions(input_file)
    matrix = Matrix(None, 1000, 1000, 10)
    # matrix = Matrix(None, 26, 26, 10, (15, 11))
    # matrix = Matrix(None, 26, 26, 10, (15, 11))
    # matrix = Matrix(None, 6, 6, 2)
    # matrix = Matrix(None, 6, 6, 10, (5, 0))
    last_instruction = instuctions[0]
    for instruction in instuctions:
        # if last_instruction != instruction:
        # if True:
        #     print(matrix)
        #     print('-'*matrix.n_cols*2)
        matrix.moveHead(instruction)
        last_instruction = instruction
    # print(matrix)
    # print('-'*matrix.n_cols*2)
    n_tail_positions = matrix.count_caracters()
    print(f'n tail positions = {n_tail_positions}')
