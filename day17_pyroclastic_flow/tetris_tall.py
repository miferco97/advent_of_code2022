import os
import sys
from itertools import cycle
from typing import List, Tuple, Union, Any, Dict


class Rock:
    def __init__(self, sprite: List, initial_position: Tuple) -> None:
        self.sprite: List = sprite
        self.position: Tuple = initial_position
        self.has_ended = False

    @property
    def left_limit(self):
        return self.position[0]

    @property
    def right_limit(self):
        return self.position[0] + len(self.sprite[0])

    @property
    def top_limit(self):
        return self.position[1] + len(self.sprite)-1

    @property
    def bottom_limit(self):
        return self.position[1]

    def move(self, direction: str):
        pass


class Chamber:
    def __init__(self) -> None:
        self.rocks: List[Rock] = []
        self.chamber: List = ['-------']
        self.top_line = [0]*7
        print(self.top_line)

    def add_rock(self, sprite: List):
        print(f'adding_rock: {sprite}')
        initial_y = len(self.chamber)+3
        self.rocks.append(Rock(sprite, (2, initial_y)))
        self.chamber.extend(['.......']*(len(sprite)+3))

    def check_end(self, rock: Rock):
        end = False
        for index, values in enumerate(self.top_line):
            if index in range(rock.left_limit, rock.right_limit):
                if rock.bottom_limit <= values+1:
                    rock.has_ended = True
                    end = True
                    self.top_line[index] = rock.top_limit
        return end

    def step(self, movement_cycle) -> bool:
        rock = self.rocks[-1]
        if rock.has_ended:
            return True
        movement = movement_cycle.__next__()
        if movement == '>' and rock.right_limit != len(self.chamber[0]):
            rock.position = (rock.position[0]+1, rock.position[1])
        elif movement == '<' and rock.left_limit != 0:
            rock.position = (rock.position[0]-1, rock.position[1])
        rock.position = (rock.position[0], rock.position[1]-1)
        if (self.check_end(rock)):
            movement = movement_cycle.__next__()
            if movement == '>' and rock.right_limit != len(self.chamber[0]):
                rock.position = (rock.position[0]+1, rock.position[1])
            elif movement == '<' and rock.left_limit != 0:
                rock.position = (rock.position[0]-1, rock.position[1])
            return True
        return False

    def __repr__(self) -> str:
        draw = ''
        basic_line = '.......'
        chamber: List = self.chamber.copy()
        # if len(self.rocks):
        #     chamber = [basic_line for x in range(self.rocks[-1].top_limit)]
        for rock in self.rocks:
            for i in range(rock.bottom_limit, rock.top_limit+1):
                line = chamber[i]
                new_line = ''
                for x, char in enumerate(line):
                    if x in range(rock.left_limit, rock.right_limit):
                        if rock.has_ended:
                            new_line = new_line+'#'
                        else:
                            new_line = new_line+'@'
                    else:
                        new_line = new_line+char
                chamber[i] = new_line

        chamber.reverse()
        for line in chamber:
            draw = draw + '|' + ' '.join(line) + '|' + '\n'
        # draw = draw + ' '.join('+-------+')
        return draw


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    visualize = False
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    command_list = []
    with open(input_file, 'r') as f:
        command_list = [char for char in f.readlines()[0].strip()]
    commands = cycle(command_list)
    rock_types_list = []
    with open('./rock_types', 'r') as f:
        rock_types_list = [y.split('\n')
                           for y in [x for x in f.read().split('\n\n')]]
    rock_types = cycle(rock_types_list)

    chamber = Chamber()

    for n_rock in range(6):
        sprite = rock_types.__next__()
        chamber.add_rock(sprite.copy())
        while(not chamber.step(commands)):
            print(chamber)
            # pass
        print(chamber)
    # chamber.add_rock(['@@@@'])
    print(chamber)
    # chamber.step('<')
    # print(chamber)
    # chamber.step('<')
    # print(chamber)
    # chamber.step('<')
    # print(chamber)
    # chamber.step('>')
    # print(chamber)
