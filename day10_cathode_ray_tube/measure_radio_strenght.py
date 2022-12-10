import os
import sys
from typing import List, Tuple
from collections import deque


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
    interest_cycles = [20, 60, 100, 140, 180, 220]
    accum_signal_strenght = 0
    for cycle in interest_cycles:
        value = register_values[cycle-1]*cycle
        print(
            f'Value of cycle {cycle} is {register_values[cycle-1]} so strength is : {value}')
        accum_signal_strenght += value
    print(f'The total strengh is {accum_signal_strenght}')
