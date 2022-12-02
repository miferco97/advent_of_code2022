import os
import sys
from typing import List
from itertools import cycle


def convert_to_R_P_S(char: str) -> str:
    rules_dict = {'A': 'R',
                  'B': 'P',
                  'C': 'S',
                  'X': 'R',
                  'Y': 'P',
                  'Z': 'S'}
    return rules_dict[char]


def choice_scoring(char: str) -> int:
    score_dict = {'R': 1, 'P': 2, 'S': 3}
    return score_dict[char]


def decide_play(oponent_play: str, strategy: str) -> str:
    if strategy == 'Y':
        return oponent_play
    rules_win = cycle(['R', 'P', 'S'])
    rules_lose = cycle(['R', 'S', 'P'])
    rules = rules_win if strategy == 'Z' else rules_lose
    a = next(rules)
    while a != oponent_play:
        a = next(rules)
    return next(rules)


def evaluate_play(oponent_play: str, our_play: str) -> int:
    our_play = decide_play(oponent_play, our_play)
    score_choice = choice_scoring(our_play)
    if oponent_play == our_play:
        return score_choice + 3  # a withdraw

    play = set()
    play.add(oponent_play)
    play.add(our_play)

    # add 3 rules
    winner = ''
    if 'R' in play and 'P' in play:
        winner = 'P'
    elif 'R' in play and 'S' in play:
        winner = 'R'
    elif 'S' in play and 'P' in play:
        winner = 'S'
    else:
        raise RuntimeError(f'this play is incorrect')

    if our_play == winner:
        return score_choice + 6
    else:
        return score_choice + 0


def parse_plays(filepath: str) -> List[List[str]]:
    plays: List[List[str]] = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            x, y = line.split(' ')
            play = [convert_to_R_P_S(x), y]
            plays.append(play)
    return plays


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)

    plays = parse_plays(input_file)
    # print(plays)
    total_score = 0
    for opponent_play, our_play in plays:
        total_score += evaluate_play(opponent_play, our_play)
    print(f'The total score will be {total_score}')
