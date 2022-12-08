import os
import sys
from typing import List, Tuple, Dict
from termcolor import colored


class Matrix():
    def __init__(self, data, n_rows, n_cols):
        self.data = data
        self.n_rows = int(n_rows)
        self.n_cols = int(n_cols)
        self.col_lims = [0, self.n_cols-1]
        self.row_lims = [0, self.n_rows-1]

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
                if self.item_is_visible(i, j):
                    items.append(colored(str(self(i, j)), 'green'))
                else:
                    items.append(colored(str(self(i, j)), 'blue'))
            repr += ' '.join(items)
            repr += '\n'
        return repr[:-1]

    def item_is_visible(self, i, j) -> bool:
        item = self(i, j)
        # border analysis
        if (i in self.row_lims) or (j in self.col_lims):
            return True
        # col analysis
        col = self.col(j)
        top_side_max = max(col[:i])
        bottom_side_max = max(col[i+1:])
        if top_side_max < item or bottom_side_max < item:
            return True
        # row analysis
        row = self.row(i)
        left_side_max = max(row[:j])
        right_side_max = max(row[j+1:])
        if left_side_max < item or right_side_max < item:
            return True
        return False

    def extract_direction_line_with_visibility(self, initial_i, initial_j, displacement_i, displacement_j) -> List[int]:
        item = self(initial_i, initial_j)
        i, j = initial_i, initial_j
        direction_list = []
        while True:
            i, j = i + displacement_i, j + displacement_j

            if ((i < 0) or (i > self.n_rows-1)) or ((j < 0) or (j > self.n_cols-1)):
                break
            temp_item = self(i, j)
            if temp_item >= item:
                direction_list.append(temp_item)
                break
            direction_list.append(temp_item)
        return direction_list

    def compute_scenic_score(self, i, j) -> int:
        score = 1
        item = self(i, j)
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for displacement_i, displacement_j in directions:
            visibility_line = self.extract_direction_line_with_visibility(
                i, j, displacement_i, displacement_j)
            # print(
            #     f'beggining in {i}, {j} tree, the visibility_line looking {displacement_i}, {displacement_j} is : \n {visibility_line}')
            score *= len(visibility_line)

        return score


def parse_tree_matrix(filepath: str) -> Matrix:
    matrix = []
    n_cols = 0
    n_rows = 0
    with open(filepath, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            row = []
            for char in line:
                row.append(char)
            n_cols = len(row)
            matrix.extend(row)
            n_rows += 1
    return Matrix(matrix, n_rows, n_cols)


def find_visible_trees(matrix: Matrix) -> int:
    visible_trees = 0
    for i in range(matrix.n_rows):
        for j in range(matrix.n_cols):
            if matrix.item_is_visible(i, j):
                visible_trees += 1
    return visible_trees


def find_the_highest_scenic_score(matrix: Matrix) -> int:
    score_set = set()
    for i in range(matrix.n_rows):
        for j in range(matrix.n_cols):
            score_set.add(matrix.compute_scenic_score(i, j))
    return max(score_set)


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    matrix = parse_tree_matrix(input_file)
    print(matrix)
    visible_trees = find_visible_trees(matrix)
    print(f'There are {visible_trees} visible trees in the grid')
    max_score = find_the_highest_scenic_score(matrix)
    print(f'The highest scenic score is {max_score}')

    # print('scenic_score=', matrix.compute_scenic_score(1, 2))
    # print('scenic_score=', matrix.compute_scenic_score(3, 2))
