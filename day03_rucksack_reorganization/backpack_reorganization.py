import sys
import os
from typing import List, Tuple


def parse_backpacks(filename: str) -> List[Tuple]:
    lines = []
    backpacks = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        line_len = len(line)
        backpacks.append((line[:line_len//2], line[line_len//2:]))
    return backpacks


def extact_common_items(backpacks: List[Tuple]) -> List[List[str]]:
    common_items: List[List[str]] = []
    for set1, set2 in backpacks:
        set1 = set(set1)
        set2 = set(set2)
        common = set1.intersection(set2)
        common_items.append(list(common))
    return common_items


def convert_to_priority(item: str) -> int:
    if item.islower():
        int_val = ord(item)-96
    else:
        int_val = ord(item)-65+27
    return int_val


def count_priorities(items: List[List[str]]) -> int:
    total = 0
    for item in items:
        for coindicende in item:
            total += convert_to_priority(coindicende)
    return total


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    backpacks = parse_backpacks(input_file)
    common_items = extact_common_items(backpacks)
    total = count_priorities(common_items)
    print(f"The total sum of the priorities is {total}")
