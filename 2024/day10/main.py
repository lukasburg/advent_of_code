from itertools import product

def read(filename):
    with open(filename) as file:
        string = file.read()[:-1]
        return string

def parse(string):
    return [[int(v) for v in line] for line in string.split("\n")]

def is_inbounds(x, y, x_max, y_max):
    return 0 <= x < x_max and 0 <= y < y_max

def render(trail_map):
    return "\n".join(["".join(list(map(str, trail_map[y]))) for y in range(len(trail_map))])

def go_up(trail_map, pos):
    x, y = pos
    current_height = trail_map[y][x]
    # print(pos, current_height)
    x_max, y_max = len(trail_map[0]), len(trail_map)
    if current_height == 9:
        # print(f"reached end at {pos}")
        return {pos}
    new_directions = [(x+x_dir, y+y_dir) for x_dir, y_dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
    in_bounds = [(x, y) for x, y in new_directions if is_inbounds(x, y, x_max, y_max)]
    in_higher = [(x_n, y_n) for x_n, y_n in in_bounds if trail_map[y_n][x_n] == current_height+1]
    results_from_next = [go_up(trail_map, new_pos) for new_pos in in_higher]
    # print(results_from_next)
    reachable = set()
    for res in results_from_next:
        reachable = reachable.union(res)
    # print(reachable)
    return reachable

def go_up_part_two(trail_map, pos):
    x, y = pos
    current_height = trail_map[y][x]
    # print(pos, current_height)
    x_max, y_max = len(trail_map[0]), len(trail_map)
    if current_height == 9:
        # print(f"reached end at {pos}")
        return 1
    new_directions = [(x+x_dir, y+y_dir) for x_dir, y_dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
    in_bounds = [(x, y) for x, y in new_directions if is_inbounds(x, y, x_max, y_max)]
    in_higher = [(x_n, y_n) for x_n, y_n in in_bounds if trail_map[y_n][x_n] == current_height+1]
    results_from_next = [go_up_part_two(trail_map, new_pos) for new_pos in in_higher]
    return sum(results_from_next)

def run(file='input.txt'):
    trail_map = parse(read(file))
    total_sum = 0
    for x, y in filter(lambda it: trail_map[it[1]][it[0]] == 0, product(range(len(trail_map[0])), range(len(trail_map)))):
        total_sum += len(go_up(trail_map, (x, y)))
    print(total_sum)
    
def run2(file='input.txt'):
    trail_map = parse(read(file))
    total_sum = 0
    for x, y in filter(lambda it: trail_map[it[1]][it[0]] == 0, product(range(len(trail_map[0])), range(len(trail_map)))):
        total_sum += go_up_part_two(trail_map, (x, y))
        # total_sum += len(go_up_part_two(trail_map, (x, y)))
    print(total_sum)

if __name__ == "__main__":
    run("example.txt")
    run()
    run2("example.txt")
    run2()
