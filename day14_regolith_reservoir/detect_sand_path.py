import os
import sys
from typing import List, Tuple, Union

SAND_POINT = (500, 0)


class Matrix():
    def __init__(self, data, n_rows, n_cols):
        self.data = data
        self.n_rows = int(n_rows)
        self.n_cols = int(n_cols)
        self.col_lims = [0, self.n_cols-1]
        self.row_lims = [0, self.n_rows-1]
        self.sand_generator = (0, 0)

    def __call__(self, i: int, j: int):
        return self.data[(i*self.n_cols)+j]

    def set(self, value, i: int, j: int):
        self.data[(i*self.n_cols)+j] = value

    def setSandGenerator(self, i: int, j: int):
        self.sand_generator = (i, j)
        self.data[(i*self.n_cols)+j] = '+'

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
                items.append(str(self(i, j)))
            repr += ' '.join(items)
            repr += '\n'
        return repr[:-1]


def parse_path_to_values(paths: List) -> List:
    values = []
    for path in paths:
        for i in range(1, len(path)):
            p1 = path[i-1]
            p2 = path[i]
            p1_x = int(p1[0])
            p1_y = int(p1[1])
            p2_x = int(p2[0])
            p2_y = int(p2[1])
            if p1_x == p2_x:
                max_y = max(p1_y, p2_y)
                min_y = min(p1_y, p2_y)
                points = list(
                    zip([p1_x]*(max_y-min_y+1), range(min_y, max_y+1)))
                values.extend(points.copy())
            elif p1_y == p2_y:
                max_x = max(p1_x, p2_x)
                min_x = min(p1_x, p2_x)
                points = list(
                    zip(range(min_x, max_x+1), [p2_y]*(max_x-min_x+1)))
                values.extend(points.copy())
            else:
                raise ValueError('something unexpected happened')
    return values


def parse_regolith(filename: str) -> Matrix:
    data = []
    n_cols = 0
    n_rows = 0
    with open(filename, 'r') as f:
        package = []
        raw_paths = [x.strip().split('->') for x in f.readlines()]
        paths = []
        for path in raw_paths:
            individual_path = []
            for elem in path:
                x, y = elem.strip().split(',')
                individual_path.append((x, y))
            paths.append(individual_path.copy())
        print(paths)

    values_list = parse_path_to_values(paths)
    print(values_list)
    x_values = [x for x, y in values_list]
    y_values = [y for x, y in values_list]
    x_values.append(SAND_POINT[0])
    y_values.append(SAND_POINT[1])

    # global SAND_POINT
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    n_cols, n_rows = max_x-min_x+1, max_y-min_y+1
    print(n_rows, n_cols)
    matrix = Matrix(['.']*n_cols*n_rows, n_rows, n_cols)
    print(matrix)
    for x, y in values_list:
        x, y = x-min_x, y-min_y
        matrix.set('#', y, x)
    matrix.setSandGenerator(SAND_POINT[1]-min_y, SAND_POINT[0]-min_x)
    return matrix


def particle_move(regolith: Matrix, particle: List) -> List:
    i, j = particle
    if regolith(i+1, j) == '.':
        return [i+1, j]
    elif regolith(i+1, j-1) == '.':
        return [i+1, j-1]
    elif regolith(i+1, j+1) == '.':
        return [i+1, j+1]
    else:
        return []


def step(regolith: Matrix) -> bool:
    s_i, s_j = regolith.sand_generator
    particle = [s_i, s_j]
    last_particle = [s_i, s_j]

    while True:
        try:
            particle = particle_move(regolith, particle)
        except:
            return False
        if particle == []:
            regolith.set('o', *last_particle)
            return True
        if particle[0] < 0 or particle[1] < 0:
            return False
        if particle[0] >= regolith.n_rows or particle[1] >= regolith.n_cols:
            return False
        else:
            last_particle = particle


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    regolith = parse_regolith(input_file)
    print(regolith)
    print('------------------------')
    while step(regolith):
        pass
    print(regolith)

    total = sum([1 for x in regolith.data if x == 'o'])
    print(f'The total number of sand particles are {total}')
