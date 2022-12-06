import os
import sys
from typing import List, Tuple
from collections import deque


def parse_dataframes(filename: str) -> List[str]:
    dataframes = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            dataframes.append(line.strip())
    return dataframes


def find_first_marker(dataframe: str, n_chars: int = 4) -> int:

    last_n_chars = deque()
    for i, character in enumerate(dataframe):
        last_n_chars.append(character)
        if len(last_n_chars) > n_chars:
            last_n_chars.popleft()
        if len(set(last_n_chars)) == n_chars:
            return i+1

    return -1


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    dataframes = parse_dataframes(input_file)
    for dataframe in dataframes:
        positition = find_first_marker(dataframe, 4)
        print(
            f'the first marker of lenght 4 is found after {positition} characters')
        positition = find_first_marker(dataframe, 14)
        print(
            f'the first marker of lenght 14 is found after {positition} characters')
