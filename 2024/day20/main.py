from collections import defaultdict, Counter

import helpers

def read(filename="input.txt"):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string) -> helpers.Map:
    return helpers.Map.from_string(string)

def set_distances_from_start(maze):
    current = maze.find_symbol('S')
    distance = 0
    path = []
    while maze[current] != 'E':
        path.append(current)
        maze[current] = distance
        distance += 1
        candidates = {current + d for d in maze.directions}
        current = next(filter(lambda c: maze[c] == '.' or maze[c] == 'E', candidates))
    # E set distance
    maze[current] = distance
    return path

def find_shortcuts(maze, original_path, radius) -> list[tuple[str, int]]:
    shortcuts = []
    for c in original_path:
        for s in maze.coords_in_radius_of(c, radius):
            # jump through possible wall
            destination_position = maze[s]
            if destination_position != '#':
                cost_savings = (destination_position - maze[c]) -helpers.distance(s, c)
                if cost_savings >= 2:
                    shortcuts.append((f'[x:{int(c.real)}, y:{int(c.imag)}]', cost_savings))
    return shortcuts

def find_bigger_shortcuts(maze: helpers.Map, original_path) -> list[tuple[str, str, int]]:
    shortcuts = []
    # for c in original_path:
    print()
    for i in maze.coords_in_radius_of(1+3j, 3):
        maze[i] = 'o'
    print(maze)
        # break

def group_by_savings(shortcuts):
    savings = Counter(map(lambda s: s[1], shortcuts))
    return savings

def run(file="input.txt", cutoff=100, radius=2):
    maze = parse(read(file))
    # shortcuts2 = find_bigger_shortcuts(maze, None)
    path = set_distances_from_start(maze)
    shortcuts = find_shortcuts(maze, path, radius)
    amount_of_shortcuts = group_by_savings(shortcuts)
    better_than_n = map(lambda s: s[1], filter(lambda s: s[0] >= cutoff, amount_of_shortcuts.items()))
    # print(list(map(lambda c: (c[1], c[0]), sorted(filter(lambda s: s[0] >= cutoff, amount_of_shortcuts.items()), key=lambda c: c[0]))))
    return sum(better_than_n)


if __name__ == "__main__":
    print(run("example.txt", 33))
    print(run())
    print(run("example.txt", 50, radius=20))
    print(run(cutoff=100, radius=20))
