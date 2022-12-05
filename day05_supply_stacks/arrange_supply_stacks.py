import os
import sys
from typing import List, Tuple,Dict

def parse_instructions(line:str)->Dict[str,int]:
    items = line.split()
    return {'move':int(items[1]),'from':int(items[3]),'to':int(items[5])}

def parse_stacks(lines:List[str])->List[List]:
    n_cols=len(lines[0])//4
    matrix_linearized=[]
    for line in lines:
        for col in range(n_cols):
            matrix_linearized.append(line[col*4+1])
    
    n_rows=len(matrix_linearized)//n_cols
    stacks=[]
    for col in range(n_cols):
        stack_col=[]
        for row in range(n_rows):
            val = matrix_linearized[col+(row*n_cols)]
            if val.strip():
                stack_col.append(val)
        stacks.append(stack_col.copy())
    return stacks


def parse_stacks_and_instructions(filename: str) -> Tuple[List[List],List[Dict[str,int]]]:
    stacks:List[List]=[]
    instructions=[]
    lines=[]
    with open(filename,'r') as f:
        lines=f.readlines()

    reading_instructions=False
    for line in lines:
        if reading_instructions:
            instructions.append(parse_instructions(line))
            continue
        if line.strip()=='':
            reading_instructions=True
        else:
            stacks.append(line)

    stacks=stacks[:-1]
    stacks.reverse()

    return parse_stacks(stacks),instructions

def follow_instructrions(stack:List[List],instructions:List[Dict[str,int]],move_together:bool=False)->List[List]:
    stack_modified = stack.copy()
    for instruction in instructions:
        move=instruction['move']
        col_modified = stack_modified[instruction['from']-1]
        items_to_move = col_modified[-move:]
        stack_modified[instruction['from']-1]=col_modified[0:-move]
        if not move_together:
            items_to_move.reverse()
        # else:
            # print(f'moving {move} items from {instruction["from"]} to {instruction["to"]}')
        stack_modified[instruction['to']-1].extend(items_to_move.copy())

    return stack_modified


def find_last_letters(stack:List[List])->List[str]:
    last_letters=[]
    string=''
    for col in stack:
        last_letters.append(col[-1])
        string+=col[-1]
    print(f'last letters are {string}')
    return last_letters

def print_stack(stack:List[List])->None:
    n_cols = len(stack)
    n_rows = 0
    for col in stack:
        if n_rows<len(col):
            n_rows=len(col)
    new_stack=[]
    for col in stack:
        new_col = []
        for i in range(n_rows):
            if (i < len(col)):
                new_col.append(f'[{col[i]}] ')
            else:
                new_col.append(f'    ')
        new_stack.append(new_col.copy())
    cols_range=list(range(n_rows))
    cols_range.reverse()
    print('-'*len(stack)*4)
    for i in cols_range:
        string =''
        for j in range(n_cols):
            string+=new_stack[j][i]
        print(string[:-1])
    print('-'*len(stack)*4)


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    stacks,instructions = parse_stacks_and_instructions(input_file)
    print('\n ORIGINAL STACKS ')
    print_stack(stacks.copy())
    print(' MODIFIED STACKS 1 BY 1 ')
    stack_modified = follow_instructrions(stacks.copy(),instructions.copy())
    print_stack(stack_modified.copy())
    last_letters=find_last_letters(stack_modified.copy())
    print(' MODIFIED STACKS MOVED_TOGETHER ')
    stacks,instructions = parse_stacks_and_instructions(input_file)
    stack_modified = follow_instructrions(stacks.copy(),instructions.copy(),True)
    print_stack(stack_modified.copy())
    last_letters=find_last_letters(stack_modified.copy())
    


