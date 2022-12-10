import os
import sys
from typing import List, Tuple
from collections import deque


class CRT:
    def __init__(self, rows=6, cols=40) -> None:
        self.n_rows = rows
        self.n_cols = cols
        self.data = ['.']*rows*cols
        self.crt_pos = 0

    def step(self, X_reg_value: int) -> None:
        X_hoz = X_reg_value % self.n_cols
        X_crt = self.crt_pos % self.n_cols
        if X_crt >= X_hoz - 1 and X_crt <= X_hoz+1:
            self.data[self.crt_pos] = '#'
        self.crt_pos += 1

    def __call__(self, i: int, j: int):
        return self.data[(i*self.n_cols)+j]

    def __repr__(self) -> str:
        repr = ''
        for i in range(self.n_rows):
            items = []
            for j in range(self.n_cols):
                items.append(self(i, j))
            repr += ' '.join(items)
            repr += '\n'
        return repr[:-1]


def parse_instructions(filename: str) -> List[Tuple]:
    instructions = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            instructions.append(tuple(line.strip().split(' ')))
    return instructions


def convert_into_atomic_instructions(instructions):
    instruction_list = []
    for item in instructions:
        if item[0] == 'addx':
            instruction_list.append(('nooop',))
            instruction_list.append(('add', item[1]))
        else:
            instruction_list.append(item)

    return instruction_list


def interpret_atomic_instructions(atomic_instructions) -> List[int]:
    register_value = 1
    register_values = [register_value]
    for instruction in atomic_instructions:
        if instruction[0] == 'add':
            register_value += int(instruction[1])
        register_values.append(register_value)
    return register_values


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    instructions = parse_instructions(input_file)
    instructions = convert_into_atomic_instructions(instructions)
    register_values = interpret_atomic_instructions(instructions)
    crt = CRT()
    for value in register_values:
        crt.step(value)
    print(crt)
