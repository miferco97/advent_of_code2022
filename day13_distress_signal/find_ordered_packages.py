from json import loads
import os
import sys
from typing import List, Tuple, Union


def find_pair(string: str, index: int = 0) -> Tuple:
    line = string[index:]
    depth = 0
    for i, char in enumerate(line):
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
            if depth == 0:
                return (index, i+index)
    return (-1, -1)


def parse_list(line: str) -> List:
    line = line.strip()[1:-1]
    index = 0
    oppening = []
    brackets_list = []

    digits = []
    while index < len(line):
        char = line[index]
        if char == '[':
            begin, end = find_pair(line, index)
            sub_str = line[begin:end+1]
            sub_list = parse_list(sub_str)
            index = end
            brackets_list.append(sub_list)
        else:
            if char not in [',', '[', ']']:
                digits.append(char)
            elif char in [',', ']']:
                if len(digits):
                    number = int(''.join(digits))
                    brackets_list.append(number)
                    digits.clear()
        index += 1
    if digits:
        number = int(''.join(digits))
        brackets_list.append(number)
    return brackets_list


def parse_packages(filename: str) -> List:
    packages = []
    with open(filename, 'r') as f:
        package = []
        for line in f.readlines():
            if not line.strip():
                packages.append(tuple(package.copy()))
                package.clear()
            else:
                package.append(parse_list(line))
        packages.append(tuple(package.copy()))
    return packages


def is_ordered(lhs, rhs) -> Union[bool, None]:
    # print(lhs, rhs)
    if isinstance(lhs, int) and isinstance(rhs, int):
        if lhs == rhs:
            # print('equal')
            return None
        return True if lhs < rhs else False
    elif isinstance(lhs, List) and isinstance(rhs, List):
        ordered = True
        for i in range(min(len(lhs), len(rhs))):
            value = is_ordered(lhs[i], rhs[i])
            # print(value)
            if value is not None:
                return value
        if len(rhs) == len(lhs):
            return None
        return True if len(lhs) < len(rhs) else False
    elif isinstance(lhs, int) and isinstance(rhs, List):
        return is_ordered([lhs], rhs)
    elif isinstance(lhs, List) and isinstance(rhs, int):
        return is_ordered(lhs, [rhs])
    return False


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    packages = parse_packages(input_file)

    packages = parse_packages(input_file)
    right_order_list = []

    for i, (lhs, rhs) in enumerate(packages, start=1):
        value = is_ordered(lhs, rhs)
        if value:
            right_order_list.append(i)
    print('The correct indices were:', right_order_list)
    print('Their sum is:', sum(right_order_list))
