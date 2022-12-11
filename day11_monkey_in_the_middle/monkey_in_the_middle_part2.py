import os
import sys
from typing import List, Tuple, Callable, Type
from collections import deque
from itertools import cycle
from tqdm import tqdm


class test:
    def __init__(self, div, true_case, false_case) -> None:
        self.true_case = int(true_case)
        self.false_case = int(false_case)
        self.div = int(div)

    def __call__(self, value: int) -> int:
        return self.true_case if value % self.div == 0 else self.false_case


class Monkey:
    def __init__(self, starting_items: List[(Tuple[str, int])], operation: str, divisibility_test: test) -> None:
        self.n_inspects = 0
        self.items = deque(starting_items)
        self.operation = self.parse_operation(operation)
        self.operation_str = operation
        self.test = divisibility_test

    def receive(self, item):
        self.items.append(item)

    def get_business(self):
        return self.n_inspects

    def get_items(self):
        return self.items.copy()

    def turn(self) -> List[Tuple[int, int]]:
        throws = []
        for i, item in enumerate(self.items.copy()):
            self.n_inspects += 1
            result = self.operation(item[1])
            # result = result//3
            throws.append(((item[0], item[1]), self.test(result)))
            self.items.popleft()
        return throws

    def __repr__(self) -> str:
        return f' items:{self.items}'
        #  \n operation:{self.operation_str}'

    def parse_operation(self, str) -> Callable:
        operations_dict = {'+': lambda a, b: a+b,
                           '-': lambda a, b: a-b,
                           '*': lambda a, b: a*b,
                           '/': lambda a, b: a*b}
        old, oppper, value = str.split('=')[-1].strip().split(' ')
        operator = operations_dict[oppper]
        if value == 'old':
            return lambda f: operator(f, f)
        else:
            return lambda f: operator(f, int(value))


def parse_monkeys_blocks(filename: str) -> List[str]:
    monkeys_blocks = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        one_liner_file = ''.join(lines)
        monkeys_blocks = one_liner_file.split('\n\n')
    return monkeys_blocks


def parse_monkeys(filename: str) -> List[Monkey]:
    monkeys_blocks = parse_monkeys_blocks(filename)
    monkeys = []
    n_item = 0
    for m_block in monkeys_blocks:
        block = m_block.splitlines()
        name = block[0]
        starting_items = []
        for x in block[1].split(':')[-1].strip().split(','):
            starting_items.append((str(n_item), int(x)))
            n_item += 1
        operation = block[2].split(':')[-1]
        div = block[3].strip().split(' ')[-1]
        true_cond = block[4].strip().split(' ')[-1]
        false_cond = block[5].strip().split(' ')[-1]
        monkeys.append(Monkey(starting_items, operation,
                       test(div, true_cond, false_cond)))

    return monkeys


def play_round(monkey_list: List[Monkey]):
    for monkey in monkey_list:
        turn = monkey.turn()
        for item, monkey in turn:
            monkey_list[monkey].receive(item)


def match_value_in_list(list_orig, list_comp):
    for i, sublist in enumerate(list_orig):
        # print(sublist, list_comp)
        # print(list_comp)
        if list_comp == sublist:
            # print(list_comp)
            print(sublist)
            return True
    return False


def get_items_list(monkeys: List[Monkey]):
    monkey_items = []
    for monkey in monkeys:
        items_str = ' '.join([x for x, y in monkey.get_items()])
        monkey_items.append(items_str)
    return ':'.join(monkey_items)


def compute_inspects_at_round(round: int, config_rounds: List[Tuple[str, List[int]]]) -> List[int]:
    period_compound = [values for name, values in config_rounds]
    period = len(period_compound)-1
    config_rounds_reformultated = []
    for monkey in range(len(period_compound[0])):
        monkey_list = []
        for i in range(1, len(period_compound)):
            monkey_list.append(
                period_compound[i][monkey]-period_compound[i-1][monkey])
        config_rounds_reformultated.append(monkey_list.copy())

    monkey_values = []

    n_times = int((round-1)/(period))
    for monkey_id in range(len(period_compound[0])):
        monkey_value = period_compound[0][monkey_id]  # round 1
        if round == 1:
            monkey_values.append(monkey_value)
            continue
        monkey_value += n_times * sum(config_rounds_reformultated[monkey_id])
        if (round+1) % period != 0 and round != 1:
            # print('entering', monkey_value)
            monkey_value += config_rounds_reformultated[monkey_id][(
                (round) % period)]
        monkey_values.append(monkey_value)

    return monkey_values


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    monkeys = parse_monkeys(input_file)
    interest_rounds = [1, 20]
    # interest_rounds = []
    rounds = []
    config_rounds = []
    for i in range(1, 100):
        play_round(monkeys)
        items_list = get_items_list(monkeys)
        if i in interest_rounds:
            print(f'Monkey_inspections were', [
                  monkey.get_business() for monkey in monkeys])
        if items_list in [x for x, n_moves in config_rounds]:
            pass
        else:
            config_rounds.append((
                items_list, [x.get_business() for x in monkeys]))

    print('result', compute_inspects_at_round(1, config_rounds))
    print('result', compute_inspects_at_round(20, config_rounds))
    print('result', compute_inspects_at_round(1000, config_rounds))
    print('result', compute_inspects_at_round(2000, config_rounds))
    print('result', compute_inspects_at_round(3000, config_rounds))
    print('result', compute_inspects_at_round(4000, config_rounds))

    monkeys_copy = monkeys.copy()
    monkeys_copy.sort(key=lambda x: x.get_business())
    print(
        f' the level of monkeys_business is : {monkeys_copy[-1].get_business() * monkeys_copy[-2].get_business()}')
