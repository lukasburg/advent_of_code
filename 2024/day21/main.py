from itertools import permutations
from functools import lru_cache

from helpers import read

numpad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
]
numpad = {
    char: complex(x, y) for y, line in enumerate(numpad) for x, char in enumerate(line)
}

keypad = [
    [None, '^', 'A'],
    ['<', 'v', '>'],
]
keypad = {
    char: complex(x, y) for y, line in enumerate(keypad) for x, char in enumerate(line)
}

def parse(string):
    return string.split("\n")

def as_str(list_of_ins_list):
    return [''.join(instruction_list) for instruction_list in list_of_ins_list]

@lru_cache
def cashed_create_instructions(start_pos, end_pos, input_dev, priorities=('<', 'v', '^', '>')):
    diff = end_pos - start_pos
    x_diff, y_diff = int(diff.real), int(diff.imag)
    x_ins = tuple('<' if x_diff < 0 else '>' for _ in range(abs(x_diff)))
    y_ins = tuple('^' if y_diff < 0 else 'v' for _ in range(abs(y_diff)))
    # catch illegal moves
    if (input_dev == 'num' and end_pos.real == 0 and start_pos.imag == 3) or (
            input_dev == 'key' and end_pos.real == 0
    ):
        # start by going up or down
        return y_ins + x_ins + tuple('A')
    elif (input_dev == 'num' and start_pos.real == 0 and end_pos.imag == 3) or (
            input_dev == 'key' and start_pos.real == 0
    ):
        # start by going left or right
        return x_ins + y_ins + tuple('A')
    elif not x_ins or not y_ins:
        # random order
        return x_ins + y_ins + tuple('A')
    elif priorities.index(x_ins[0]) < priorities.index(y_ins[0]):
        return x_ins + y_ins + tuple('A')
    else:
        return y_ins + x_ins + tuple('A')

def create_sequence_for_target(target: tuple[str], input_device, priorities=('<', 'v', '^', '>')):
    instructions = tuple()
    for current, destination in zip(tuple('A') + target, target):
        start_pos = input_device[current]
        end_pos = input_device[destination]
        inp_dev = 'key' if input_device == keypad else 'num'
        instructions += cashed_create_instructions(start_pos, end_pos, inp_dev, priorities)
    return instructions

class TargetWithPrio:
    def __init__(self, target: tuple[str], prios: list[list[str]]):
        self.target = target
        self.prios = prios

    def __len__(self):
        return len(self.target)

    def __iter__(self):
        return iter(self.target)

    def __hash__(self):
        return hash(self.target)

    def __eq__(self, other):
        return self.target == other.target

    def __repr__(self):
        return f'T(depth={len(self.prios)}, len={len(self.target)})'

def iterative_run(target_code, r=2):
    s = create_sequence_for_target(tuple(target_code), numpad)
    for _ in range(r):
        s = create_sequence_for_target(s, keypad)
    return len(s)

def run(file="input.txt"):
    target_codes = parse(read(file))
    scores = []
    scores2 = []
    for target_code in target_codes:
        score = iterative_run(target_code)
        scores.append(score * int(target_code[:-1]))
    print(scores)
    for target_code in target_codes:
        score2 = iterative_run(target_code, 25)
        scores2.append(score2 * int(target_code[:-1]))
        print(scores2)
    print(scores2)
    return sum(scores), sum(scores2)

if __name__ == "__main__":
    print(run("example.txt"))
    print(run())
