import os
import sys
from typing import List, Tuple


def parse_list(line: str) -> List:
    line = line.strip()
    # line_content = []
    print('line',line)
    index = 0
    oppening=[]
    brackets_list = []

    while index < len(line):
        char = line[index]
        if char == '[':
            oppening.append(index)
            print('line',line , 'index',index)
        elif char == ']':
            begin_index = oppening.pop()
            # sub_list =  line[begin_index:index+1]
            if len(oppening) != 0:
                sub_list =  parse_list(line[begin_index:index+1])
                index = line.find(']',index) 
                print('sub_list' , sub_list, ' :len ', len(sub_list))
                brackets_list.append(sub_list)
        else:
            if char not in [',', '[', ']'] and len(oppening) == 1:
                brackets_list.append(char)
        index += 1

    return brackets_list


def parse_packages(filename: str) -> List:
    packages = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        # parsed =parse_list(lines[3])
        parsed = parse_list(lines[22])
        print('parsed',parsed)
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
