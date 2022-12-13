import os
import sys
from typing import List, Tuple, Callable, Type, Any
from collections import deque
from tqdm import tqdm

INVERT_LOGIC = False


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
                items.append(str(self(i, j)))
            repr += ' '.join(items)
            repr += '\n'
        return repr[:-1]


def parse_height_graph(filename: str) -> Matrix:
    with open(filename, 'r') as f:
        lines = f.readlines()
        n_rows = len(lines)
        n_cols = len(lines[0].strip())
        data = ''.join([x.strip() for x in lines])
    return Matrix(data, n_rows, n_cols)


directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]


class Node():
    def __init__(self, i, j, height, parent: Any = None) -> None:
        self.height = height
        self.position = (i, j)
        self.parent = parent
        self.cost = self.parent.get_cost() + 1 if self.parent is not None else 0

    def __repr__(self) -> str:
        return f'[{self.position}]: height[{self.height}]'

    def get_cost(self):
        return self.cost

    def is_goal(self):
        if INVERT_LOGIC:
            return True if self.height == 'a' or self.height == 'S' else False
        else:
            return True if self.height == 'E' else False

    def get_value(self):
        return self.parse_height_into_value(self.height)

    def get_position(self):
        return self.position

    def get_name(self):
        return f'[{self.position[0]},{self.position[1]}]'

    def parse_height_into_value(self, height: str):
        if height == 'E':
            height = 'z'
        elif height == 'S':
            height = 'a'
        return ord(height)-ord('a')

    def get_sons(self, matrix: Matrix) -> List:
        sons = []
        for i_inc, j_inc in directions:
            i, j = self.position
            i_coord = i+i_inc
            j_coord = j+j_inc
            if i_coord < 0 or i_coord > matrix.n_rows-1:
                continue
            elif j_coord < 0 or j_coord > matrix.n_cols-1:
                continue
            # print(f'looking for {i_coord}, {j_coord}')
            if INVERT_LOGIC:
                if self.get_value() - 1 > self.parse_height_into_value(matrix(i_coord, j_coord)):
                    continue
            else:
                if self.get_value() < self.parse_height_into_value(matrix(i_coord, j_coord)) - 1:
                    continue
            sons.append(Node(i_coord, j_coord, height=matrix(
                i_coord, j_coord), parent=self))
        # print('sons:', sons)
        return sons


def get_initial_node(matrix: Matrix):
    for i in range(matrix.n_rows):
        for j in range(matrix.n_cols):
            if INVERT_LOGIC:
                if matrix(i, j) == 'E':
                    return Node(i, j, 'z', None)
            else:
                if matrix(i, j) == 'S':
                    return Node(i, j, 'a', None)
    return None


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if len(sys.argv) > 2:
            if sys.argv[2] == '--invert':
                INVERT_LOGIC = True
                print('Inverting logic')
            else:
                print('If want to invert write --invert')
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    height_matrix = parse_height_graph(input_file)
    visited_nodes = {}
    initial_node = get_initial_node(height_matrix)
    if initial_node is None:
        print('ERROR with initial node')
        exit(1)
    nodes_to_visit = [initial_node]
    end_node = None
    total_nodes = height_matrix.n_cols*height_matrix.n_rows
    n_visited = 0
    while len(nodes_to_visit):
        node = nodes_to_visit[0]
        if visited_nodes.get(node.get_name(), None) is not None:
            nodes_to_visit.pop(0)
            continue
        if node.is_goal():
            print('GOAL REACHED')
            end_node = node
            break
        # print(node)
        visited_nodes[node.get_name()] = node
        nodes_to_visit.pop(0)
        n_visited += 1
        # print(f'{n_visited}/{total_nodes}')
        # print(f'{len(visited_nodes)}/{total_nodes}')
        for son_node in node.get_sons(height_matrix):
            if son_node.is_goal():
                end_node = son_node
                print('GOAL REACHED')
                nodes_to_visit.clear()
                break
            if visited_nodes.get(son_node.get_name(), None) is not None:
                continue
            else:
                nodes_to_visit.append(son_node)
        # print('nodes_to_visit', nodes_to_visit)
        # print('nodes_visited', visited_nodes.keys())
        nodes_to_visit.sort(key=lambda x: x.get_cost())

    print(end_node)
    n_steps = 0
    parent: Node = end_node.parent
    while parent is not None:
        n_steps += 1
        parent = parent.parent
    print(n_steps)
