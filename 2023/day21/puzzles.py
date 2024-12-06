from typing import Optional

with open('input') as file:
    inp = file.read()


STEPS = 64
Coord = tuple[int, int]
Garden = list[list[Optional[str]]]


def parse_input(string_input: str) -> Garden:
    parsed_map = [[None] + list(line) + [None] for line in string_input.split('\n')]
    padding_top_bottom = [None for i in range(len(parsed_map[0]))]
    return [padding_top_bottom] + parsed_map + [padding_top_bottom]


def render_garden(garden: Garden):
    print('\n'.join([''.join(line[1:-1]) for line in garden[1:-1]]))

def find_start(garden: Garden) -> Coord:
    for y, row in enumerate(garden):
        for x, symbol in enumerate(row):
            if symbol == "S":
                return x, y


def find_all_neighbors(coordinates: set):
    neighbors = set()
    for x, y in coordinates:
        n = {
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1),
        }
        neighbors = neighbors.union(n)
    return neighbors


def filter_rocks(reachable: set[Coord], garden: Garden) -> set[Coord]:
    return set(filter(lambda c: garden[c[1]][c[0]] == '.', reachable))


def fill_reachable_with_symbol(reachable: set[Coord], garden: Garden, symbol='x'):
    for x, y in reachable:
        garden[y][x] = symbol


def run(string_input: str, steps: int):
    garden = parse_input(inp)
    start = find_start(garden)
    # start is also visitable
    garden[start[1]][start[0]] = '.'
    reachable_now = {start}
    for i in range(1, steps+1):
        new_reachable = find_all_neighbors(reachable_now)
        reachable_now = filter_rocks(new_reachable, garden)
        # print(f'After {i} steps: \n')
        # render_garden(garden)
    fill_reachable_with_symbol(reachable_now, garden, 'O')
    render_garden(garden)
    print(f'Reachable after {i} steps: {len(reachable_now)}')


if __name__ == "__main__":
    run(inp, STEPS)
