import numpy as np

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def add_coords(v1, v2):
        return v1[0] + v2[0], v1[1] + v2[1]

instruction_to_direction = {'^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1)}
direction_to_instruction = {v: k for k, v in instruction_to_direction.items()}


def parse(string):
    warehouse_str, instructions_str = string.split("\n\n")
    lines = warehouse_str.split("\n")
    x_len, y_len = len(lines[0]), len(lines)
    warehouse = np.full((x_len, y_len),'.', dtype=np.dtype('U1'))
    start_pos = -1, -1
    for x, line in enumerate(lines):
        for y, sym in enumerate(line):
            if sym in ('#', 'O'):
                warehouse[x, y] = sym
            if sym == '@':
                start_pos = x, y
    instructions = [instruction_to_direction[it] for line in instructions_str.split('\n') for it in line]
    return warehouse, instructions, start_pos


def render_warehouse(warehouse, r_pos):
    previous = warehouse[r_pos]
    if previous == '.':
        warehouse[r_pos] = '@'
    else:
        warehouse[r_pos] = previous.lower()
    print(warehouse)
    warehouse[r_pos] = previous

class IsBlockedError(ValueError):
    pass

def move_box(next_pos, direction, warehouse):
    try:
        if direction in {(1, 0), (-1, 0)}:
            sliced = slice(next_pos[0],None,direction[0])
            line = warehouse[sliced, next_pos[1]]
        if direction in {(0, 1), (0, -1)}:
            sliced = slice(next_pos[1],None,direction[1])
            line = warehouse[next_pos[0], sliced]
        first_wall = next((idx for idx, val in np.ndenumerate(line) if val=='#'))[0]
        line = line[:first_wall]
        first_empty_space_relativ_pos = next((idx for idx, val in np.ndenumerate(line) if val=='.'))
        line[first_empty_space_relativ_pos] = 'O'
        warehouse[next_pos] = '.'
    except StopIteration:
        raise IsBlockedError

def move(pos, direction, warehouse):
    next_pos = add_coords(pos, direction)
    if warehouse[next_pos] == '#':
        raise IsBlockedError
    elif warehouse[next_pos] == 'O':
        move_box(next_pos, direction, warehouse)
    return next_pos

def gps(pos):
    return pos[0] * 100 + pos[1]


def run(file="input.txt"):
    warehouse, instructions, pos = parse(read(file))
    for direction in instructions:
        try:
            pos = move(pos, direction, warehouse)
        except IsBlockedError:
            pass
    boxes = zip(*np.where(warehouse == 'O'))
    render_warehouse(warehouse, pos)
    return sum(map(gps, boxes))


if __name__ == "__main__":
    print(run("example.txt"))
    print(run())
    # run()
