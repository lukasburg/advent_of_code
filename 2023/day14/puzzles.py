from pprint import pprint

import numpy

with open("input") as file:
    inp = [list(line[:-1]) for line in file.readlines()]


def calculate_load(grid):
    total_load = 0
    for y, row in enumerate(grid):
        y = len(grid) - y
        total_load += y * len(list(filter(lambda s: s=='O', row)))
    return total_load


def render_grid(grid):
    print()
    for row in grid:
        print(''.join(row))


def tilt_row(row):
    new_row = []
    free_space_index = len(row)
    for y, symbol in enumerate(row):
        y = len(row) - y
        # print(y, free_space_index, symbol)
        if symbol == 'O':
            # print(f'Takes {free_space_index}')
            free_space_index -= 1
            new_row.append('O')
        if symbol == '#':
            new_row += ['.' for i in range(free_space_index-y)] + ['#']
            free_space_index = y - 1
            # print(f'Puts boundary at {free_space_index}')
    new_row += ['.' for i in range(free_space_index)]
    return new_row


def tilt_grid(grid):
    new_grid = []
    for row in grid:
        new_row = tilt_row(row)
        new_grid.append(new_row)
        # print(f'{row}  ->  {new_row}')
    return new_grid


def cycle_grid(grid):
    for i in range(4):
        grid = tilt_grid(grid)
        # print(f'\n\n{i}:\n')
        # render_grid(grid)
        grid = numpy.rot90(grid, k=3)
    return grid


def hash_grid(grid):
    return '\n'.join([''.join(row) for row in grid])


# print(tilt_grid(inp))
current_grid = numpy.rot90(inp)
# final_grid = tilt_grid(final_grid)
# render_grid(final_grid)
# render_grid(numpy.rot90(final_grid, k=3))
# print(calculate_load(numpy.rot90(final_grid, k=3)))
# render_grid(initial_grid)

variation_number = dict()
variations = []
variation_counter = 0
cycle_for = 1000000000
for i in range(cycle_for):
    current_grid = cycle_grid(current_grid)
    if hash_grid(current_grid) not in variation_number:
        variation_number[hash_grid(current_grid)] = variation_counter
        variation_counter += 1
    elif hash_grid(current_grid) in variation_number:
        first_repetition = variation_number[hash_grid(current_grid)]
        repetition_length = i-variation_number[hash_grid(current_grid)]
        initial_chaotic_cycles = variation_number[hash_grid(current_grid)]
        print(f'Repeats after {i} steps, start: {first_repetition},'
              f' length: {repetition_length}, cycles before: {initial_chaotic_cycles}')
        final_cycle = ((cycle_for-initial_chaotic_cycles) % repetition_length) + initial_chaotic_cycles - 1
        final_cycle = final_cycle+repetition_length if final_cycle < 0 else final_cycle
        print(f'Final grid will be at position {final_cycle}: {variations[final_cycle]}')
        final_grid_str = list(variation_number.keys())[list(variation_number.values()).index(final_cycle)]
        real_final_grid = [list(row) for row in final_grid_str.split('\n')]
        final_grid_to_north = numpy.rot90(real_final_grid, k=3)
        print(f"final load {calculate_load(final_grid_to_north)}")
        break
    variations.append(variation_number[hash_grid(current_grid)])

calculate_load(current_grid)
