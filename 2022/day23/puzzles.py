from collections import defaultdict

with open('input') as file:
    inp = file.readlines()


def p_add(p1: tuple[int, int], p2: tuple[int, int]):
    return p1[0] + p2[0], p1[1] + p2[1]


def is_isolated(elf, occupied):
    neighbors = [(-1, 0), (-1, -1), (-1, 1), (1, 0), (1, -1), (1, 1), (0, 1), (0, -1)]
    return all([p_add(elf, direction) not in occupied for direction in neighbors])


def propose_new_point(elf, direction_order, occupied):
    for directions in direction_order:
        if all([p_add(elf, direction) not in occupied for direction in directions]):
            return p_add(elf, directions[1])
    return None


def find_bounds(points):
    all_x = sorted([p[0] for p in points])
    x_min, x_max = all_x[0], all_x[-1]
    all_y = sorted([p[1] for p in points])
    y_min, y_max = all_y[0], all_y[-1]
    return (x_min, x_max), (y_min, y_max)


def format_map(points):
    xbounds, ybounds = find_bounds(points)
    y_min, y_max = ybounds
    x_min, x_max = xbounds
    total_string = ''
    for y in range(y_min, y_max+1):
        line = ''.join(['#' if (x, y) in points else '.' for x in range(x_min, x_max+1)])
        total_string += line + '\n'
    return total_string


def empty_ground_in_smallest_rectangle(occupied):
    x_bounds, y_bounds = find_bounds(occupied)
    x_len = x_bounds[1] - x_bounds[0]+1
    y_len = y_bounds[1] - y_bounds[0]+1
    area = x_len*y_len
    return area - len(occupied)


def main():
    current_direction_order = [
        ((1, -1), (0, -1), (-1, -1)),  # N, NE, NW
        ((1, 1), (0, 1), (-1, 1)),     # S, SE, SW
        ((-1, -1), (-1, 0), (-1, 1)),  # W, NW, SW
        ((1, -1), (1, 0), (1, 1))      # E, NE, SE
    ]

    occupied = set()
    for y, row in enumerate(inp):
        for x, symbol in enumerate(row.strip()):
            if symbol == '#':
                occupied.add((x, y))
    print(format_map(occupied))

    all_isolated = False
    rounds = 0
    while not all_isolated:
        rounds += 1
        proposed = defaultdict(lambda: [])  # dict of new_point -> [old_points]
        no_move = set()
        all_isolated = True
        for elf in occupied:
            if is_isolated(elf, occupied):
                no_move.add(elf)
            else:
                all_isolated = False
                new_point = propose_new_point(elf, current_direction_order, occupied)
                if new_point:
                    proposed[new_point].append(elf)
                else:
                    no_move.add(elf)
        new_occupied = set()
        for new, olds in proposed.items():
            if len(olds) == 1:
                new_occupied.add(new)
            else:
                new_occupied.update(olds)
        occupied = new_occupied.union(no_move)
        current_direction_order = current_direction_order[1:] + [current_direction_order[0]]
        # print(format_map(occupied))
    print(empty_ground_in_smallest_rectangle(occupied))
    print(f'Number of rounds: {rounds}')


main()
