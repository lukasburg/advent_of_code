def get_input(filename="input"):
    with open(filename) as file:
        return file.read()


class Wall:
    def __init__(self, additional_wall = False):
        self.additional_wall = additional_wall

    def __repr__(self):
        return "O" if self.additional_wall else "#"


class Space:
    def __init__(self):
        self.visited = False
        self.visited_facing_directions = set()

    def __repr__(self):
        return "X" if self.visited else "."


class Guard:
    def __init__(self, start_pos: tuple[int, int]):
        self.direction = (0, -1)
        self.position = start_pos

    def turn(self):
        match self.direction:
            case (0, -1):
                self.direction = (1, 0)
            case (1, 0):
                self.direction = (0, 1)
            case (0, 1):
                self.direction = (-1, 0)
            case (-1, 0):
                self.direction = (0, -1)
            case _:
                raise RuntimeError

    def __repr__(self):
        return "^"

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def next_position(self):
        return self.position[0] + self.direction[0], self.position[1] + self.direction[1]


def parse_input(string):
    lab_map = []
    for y, line in enumerate(string.split("\n")[:-1]):
        lab_map.append([])
        for x, symbol in enumerate(line):
            if symbol == "#":
                lab_map[-1].append(Wall())
            elif symbol == "^":
                start_space = Space()
                start_space.visited = True
                lab_map[-1].append(start_space)
                guard = Guard((x, y))
            else:
                lab_map[-1].append(Space())
    return lab_map, guard


def render_map(lab_map):
    return "\n".join(["".join([str(s) for s in line]) for line in lab_map])


def position_inside_map(position: tuple[int, int], lab_map):
    return 0 <= position[0] < len(lab_map[0]) and 0 <= position[1] < len(lab_map)


def count_visited(lab_map):
    total = 0
    for line in lab_map:
        for space in line:
            if isinstance(space, Space):
                if space.visited:
                    total += 1
    return total


def run_part1():
    lab_map, guard = parse_input(get_input())
    while position_inside_map(guard.next_position(), lab_map):
        next_x, next_y = guard.next_position()
        next_position = lab_map[next_y][next_x]
        if isinstance(next_position, Space):
            next_position.visited = True
            guard.position = guard.next_position()
        elif isinstance(next_position, Wall):
            guard.turn()
        else:
            raise RuntimeError
        # print("\n")
        # print(render_map(lab_map))
    print(count_visited(lab_map))
    return lab_map


def run_until_loop_found(lab_map, guard):
    loopable = False
    while position_inside_map(guard.next_position(), lab_map):
        next_x, next_y = guard.next_position()
        next_position = lab_map[next_y][next_x]
        if isinstance(next_position, Space):
            if guard.direction in next_position.visited_facing_directions:
                loopable = True
                break
            next_position.visited = True
            guard.position = guard.next_position()
            next_position.visited_facing_directions.add(guard.direction)
        elif isinstance(next_position, Wall):
            guard.turn()
        else:
            raise RuntimeError
        # print("\n")
        # print(render_map(lab_map))
    return loopable


def additional_object_locations(lab_map):
    for y in range(len(lab_map)):
        print(f"trying line {y} of {len(lab_map)}")
        for x in range(len(lab_map[0])):
            yield x, y


def run_part2(unmodified_map):
    loopable_count = 0
    for x, y in additional_object_locations(unmodified_map):
        if isinstance(unmodified_map[y][x], Space) and not unmodified_map[y][x].visited:
            continue
        lab_map, guard = parse_input(get_input())
        lab_map[y][x] = Wall(True)
        loopable = run_until_loop_found(lab_map, guard)
        if loopable:
            # print(render_map(lab_map))
            loopable_count += 1
            # print(f"Found loop. Loop count: {loopable_count}")
    print(loopable_count)


if __name__ == "__main__":
    unmodified_map = run_part1()
    run_part2(unmodified_map)
