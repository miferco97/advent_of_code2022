import os
import sys
from itertools import cycle
from typing import List, Tuple, Union, Any, Dict
from tqdm import tqdm

class Rock:
    def __init__(self, sprite: List, initial_position: Tuple) -> None:
        self.sprite: List = sprite
        self.position: Tuple = initial_position
        self.has_ended = False

    @property
    def left_limit(self):
        return self.position[0]
    
    @property
    def height(self):
        return len(self.sprite)

    @property
    def length(self):
        return len(self.sprite[0])

    @property
    def right_limit(self):
        return self.position[0] + len(self.sprite[0])-1

    @property
    def top_limit(self):
        return self.position[1] + len(self.sprite)-1

    @property
    def bottom_limit(self):
        return self.position[1]

    def move(self, direction:Tuple[int,int], rocks_lists):
        new_x = self.position[0] + direction[0]
        if new_x < 0 or new_x+self.length > 7:
            return False
        new_y = self.position[1] + direction[1]
        if new_y < 0:
            return False
        if len(rocks_lists) > 100:
            for rock in rocks_lists[-99:-1]:
                if rock.check_collision(Rock(self.sprite,(new_x,new_y))):
                    # print(f'returning False rock, collision_pixel = {(new_x,new_y)}')n
                    return False
        else:
            for rock in rocks_lists[:-1]:
               if rock.check_collision(Rock(self.sprite,(new_x,new_y))):
                    # print(f'returning False rock, collision_pixel = {(new_x,new_y)}')n
                    return False
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])
        return True

    def check_position(self, position):
        if position[1] > self.top_limit+1:
            return False
        # print(self.sprite)
        for px,x in enumerate(range(self.left_limit,self.right_limit+1)):
            for py,y in enumerate(range(self.bottom_limit,self.top_limit+1)):
                if self.sprite[py][px] != '.' and (x == position[0] and y == position[1]):
                    # print(f'{px=},{py=} = {self.sprite[py][px]} collide with {position}')
                    return True
        return False

    def check_collision(self, other):
        if other.top_limit +1 < self.bottom_limit:
            return False
        for px,x in enumerate(range(self.left_limit,self.right_limit+1)):
            for py,y in enumerate(range(self.bottom_limit,self.top_limit+1)):
                if self.sprite[py][px] != '.' and other.check_position((x,y)):
                    return True
        return False

class Chamber:
    def __init__(self) -> None:
        self.rocks: List[Rock] = []
        self.chamber: List = []
        self.down=False

    @property
    def higher_y(self):
        return max([rock.top_limit for rock in self.rocks])+1 if self.rocks else 0


    def add_rock(self, sprite: List):
        self.rocks.append(Rock(sprite, (2, self.higher_y+3)))
        if len(self.chamber) < self.higher_y:
            self.chamber.extend(['.......']*(self.higher_y - len(sprite)+2))
        self.down =False
        # print('new rock appeared:')
        # print(self)

    def step(self, movement_cycle) -> bool:
        rock = self.rocks[-1]
        if rock.has_ended:
            return True
        if self.down:
            self.down=False
            if rock.move((0,-1),self.rocks):
                # print('falling')
                return False
            else:
                rock.has_ended=True
                return True
        self.down=True
        movement = next(movement_cycle)
        movement_dict={'>':(1,0),'<':(-1,0)}
        rock.move(movement_dict[movement],self.rocks)
        return False

    def __repr__(self) -> str:
        draw = ''
        basic_line = '.......'
        chamber: List = self.chamber.copy()
        for rock in self.rocks:
            for i in range(rock.bottom_limit, rock.top_limit+1):
                line = chamber[i]
                new_line = ''
                for x, char in enumerate(line):
                    if x in range(rock.left_limit, rock.right_limit+1) and \
                            rock.sprite[i-rock.bottom_limit][x-rock.left_limit] != '.' :
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
        draw = draw + ' '.join('+-------+')
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
        for _rock in rock_types_list:
            _rock.reverse()
    rock_types = cycle(rock_types_list)
    chamber = Chamber()

    for n_rock in tqdm(range(2022)):
        sprite = next(rock_types)
        # print(sprite)
        chamber.add_rock(sprite.copy())
        while(not chamber.step(commands)):
            # print(chamber)
            pass
        # print(chamber)
    print(chamber.higher_y)
