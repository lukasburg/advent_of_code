import re

from helpers import *

def parse(string) -> list[tuple[int, int]]:
    return [tuple([int(x) for x in re.match(r'(\d+),(\d+)', s).groups()]) for s in string.split('\n')]

def find_path_length_part_1(ram, falling_bytes, falling_bytes_amount, start_pos, end_pos):
    for byte in falling_bytes[:falling_bytes_amount]:
        ram[byte] = '#'
    shortest_path_length = ram.distance_search(start_pos, end_pos)
    return shortest_path_length

def fall_bytes_until_not_reachable_anymore(ram, falling_bytes, falling_bytes_amount, start_pos, end_pos):
    for byte in falling_bytes[falling_bytes_amount:]:
        ram[byte] = '#'
        try:
            ram.distance_search(start_pos, end_pos)
        except ValueError:
            return byte

def run(file='input.txt', map_size=71, falling_bytes_amount=1024):
    ram = Map.empty_map(map_size)
    start_pos = 0, 0
    end_pos = map_size-1, map_size-1
    falling_bytes = parse(read(file))
    shortest_path_length = find_path_length_part_1(ram, falling_bytes, falling_bytes_amount, start_pos, end_pos)
    first_cutoff_byte = fall_bytes_until_not_reachable_anymore(ram, falling_bytes, falling_bytes_amount, start_pos, end_pos)
    return shortest_path_length, ','.join(map(str, first_cutoff_byte))

if __name__ == '__main__':
    print(run('example.txt', map_size=7, falling_bytes_amount=12))
    print(run())
