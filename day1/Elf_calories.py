import sys
import os
from typing import List, Tuple

class CaloriesList:
    max_value = 0
    min_value = 0
    internal_list: List[tuple] = []

    def recursive_search(self, lower_index: int, higher_index: int, value: int):
        if higher_index == lower_index + 1:
            if self.internal_list[higher_index][0] < value:
                return higher_index + 1
            else:
                return lower_index if self.internal_list[lower_index][0] > value else lower_index + 1
        if higher_index == lower_index:
            return lower_index if self.internal_list[lower_index][0] > value else lower_index + 1

        search_index = (higher_index + lower_index) // 2
        search_value = self.internal_list[search_index][0]
        if (value > self.internal_list[search_index][0]):
            return self.recursive_search(search_index, higher_index, value)
        elif (value < self.internal_list[search_index][0]):
            return self.recursive_search(lower_index, search_index, value)
        else:
            return search_index

    def __getitem__(self, i):
        return self.internal_list[i]

    def __len__(self):
        return len(self.internal_list)

    def search(self, calories) -> int:
        if calories >= self.max_value:
            self.max_value = calories
            if (len(self.internal_list) == 0):
                self.min_value = calories
            return len(self.internal_list)
        if calories <= self.min_value:
            self.min_value = calories
            if (len(self.internal_list) == 0):
                self.max_value = calories
            return 0
        return self.recursive_search(0, len(self.internal_list)-1, calories)

    def insert_item(self, item: Tuple[int, str]):
        value, name = item
        insertion_index = self.search(value)
        self.internal_list.insert(insertion_index, item)


def parse_calories_list(filepath) -> CaloriesList:
    list = CaloriesList()
    lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    elf_number = 1
    calories_value = 0
    for line in lines:
        line = line.strip()
        if line == "":
            item = (calories_value, f"elf_{elf_number}")
            list.insert_item(item)
            elf_number += 1
            calories_value = 0
            continue
        value = line.strip()
        calories_value += int(value)
    item = (calories_value, f"elf_{elf_number}")
    list.insert_item(item)
    return list


def test_assertion(cal_list: CaloriesList, value: int):
    item = cal_list[cal_list.search(value)]
    print(
        f'the elf with the nearest calories to {value} from below is {item[1]} with {item[0]} ')


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    cal_list = parse_calories_list(input_file)

    # print(cal_list.internal_list[-1])
    # test_assertion(cal_list, 6000)
    # test_assertion(cal_list, 11100)

    calories_elf = cal_list.internal_list[-1]
    print(
        f'the Elf with more calories is {calories_elf[1]}, with {calories_elf[0]} calories')
