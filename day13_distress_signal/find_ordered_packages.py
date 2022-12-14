import os
import sys
from typing import List, Tuple


def parse_list(line: str) -> List:
    line = line.strip()
    begin = line.find('[')
    line_content = []
    print(line)
    index = 0
    while index < len(line):
        print(line, index)
        char = line[index]
        if char == '[' and index != 0:
            sub_list = parse_list(line[index:])
            index += len(sub_list)+1
            line_content.append(sub_list)
        elif char == ']':
            return line_content
        else:
            if char not in [',', '[', ']']:
                line_content.append(char)
        index += 1

    return []


def parse_packages(filename: str) -> List:
    packages = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        parsed = parse_list(lines[3])
        print(parsed)
        # for line in
        #     pass

    return packages


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    packages = parse_packages(input_file)
