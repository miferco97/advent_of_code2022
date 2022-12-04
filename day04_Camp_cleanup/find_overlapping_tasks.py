import os
import sys
from typing import List, Tuple


def parse_elves_tasks(filename: str) -> List[List]:
    elves_tasks = []
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        elves_task = line.strip().split(',')
        elves_sets = []
        for elf in elves_task:
            begin, end = elf.split('-')
            elf_range = set(range(int(begin), int(end)+1))
            elves_sets.append(elf_range)
        elves_tasks.append(elves_sets.copy())

    return elves_tasks


def count_fully_contained_tasks(elves_tasks: List[List]) -> int:
    task_fully_contained = 0
    for elf1, elf2 in elves_tasks:
        if elf1.issubset(elf2) or elf2.issubset(elf1):
            task_fully_contained += 1
    return task_fully_contained


def count_overlaped_ranges(elves_tasks: List[List]) -> int:
    overlaped_ranges = 0
    for elf1, elf2 in elves_tasks:
        if set.intersection(elf1, elf2):
            overlaped_ranges += 1
    return overlaped_ranges


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    elves_tasks = parse_elves_tasks(input_file)
    count = count_fully_contained_tasks(elves_tasks)
    print(
        f'The are {count} elves that have their tasks fully contained in his partner tasks')
    count_overlap = count_overlaped_ranges(elves_tasks)
    print(f'The are {count_overlap} overlapping assigments')
