import os
import sys
from typing import List, Tuple, Callable, Type
from collections import deque
from tqdm import tqdm

MCM = 1


class test:
    def __init__(self, div, true_case, false_case) -> None:
        self.true_case = int(true_case)
        self.false_case = int(false_case)
        self.div = int(div)

    def __call__(self, value: int) -> int:
        return self.true_case if value % self.div == 0 else self.false_case


class Monkey:
    def __init__(self, starting_items: List[int], operation: str, divisibility_test: test) -> None:
        self.n_inspects = 0
        self.items = deque(starting_items)
        self.operation = self.parse_operation(operation)
        self.operation_str = operation
        self.test = divisibility_test
        global MCM
        MCM *= self.test.div

    def receive(self, item):
        self.items.append(item)

    def get_business(self):
        return self.n_inspects

    def turn(self) -> List[Tuple[int, int]]:
        throws = []
        for i, item in enumerate(self.items.copy()):
            self.n_inspects += 1
            result = self.operation(item)
            # result = result//3
            global MCM
            result = result % MCM
            throws.append((result, self.test(result)))
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
    for m_block in monkeys_blocks:
        block = m_block.splitlines()
        name = block[0]
        starting_items = [int(x)
                          for x in block[1].split(':')[-1].strip().split(',')]
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


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    monkeys = parse_monkeys(input_file)
    print(monkeys)
    interest_rounds = [1, 20, 1000, 2000, 3000, 10000]
    # for i in range(1, 21):
    for i in range(1, 10001):
        play_round(monkeys)
        if i in interest_rounds:
            print(f'== After round {i} ==')
            for j, monkey in enumerate(monkeys):
                print(
                    f'Monkey {j} inspected items {monkey.get_business()} times')

    monkeys_copy = monkeys.copy()
    monkeys_copy.sort(key=lambda x: x.get_business())
    print(monkeys_copy)

    print(
        f' the level of monkeys_business is : {monkeys_copy[-1].get_business() * monkeys_copy[-2].get_business()}')
