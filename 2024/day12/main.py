import itertools
from copy import copy

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    return Garden([[cell for cell in line] for line in string.split("\n")])

class Coord:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}|{self.y})"

    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        return Coord(self.x + other[0], self.y + other[1])

    def neighbors(self):
        return {Coord(self.x + x, self.y + y) for x, y in self.directions}

    def is_inbounds(self, garden: "Garden"):
        return 0 <= self.x < garden.x_max and 0 <= self.y < garden.y_max

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class ClockwiseIterator:
    def __init__(self):
        self.i = 1

    def __iter__(self):
        return self

    def __next__(self):
        """Returns direction for line and outwards direction"""
        self.i = (self.i + 1) % 4
        return Coord.directions[self.i], Coord.directions[self.i-1]


class Garden:
    def __init__(self, garden):
        self.garden = garden
        self.x_max = len(garden[0])
        self.y_max = len(garden)

    def __getitem__(self, k: Coord | tuple):
        if isinstance(k, Coord):
            return self.garden[k.y][k.x]
        return self.garden[k[1]][k[0]]

    def __setitem__(self, k: Coord | tuple, value):
        if isinstance(k, Coord):
            self.garden[k.y][k.x] = value
        else:
            self.garden[k[1]][k[0]] = value

    def __iter__(self):
        return iter(self.garden)


def render(garden):
    return "\n".join(["".join([cell for cell in line]) for line in garden])

def flood_fill(garden, start: Coord):
    area = {start}
    symbol = garden[start]
    to_check = {start}
    checked = set()
    while to_check:
        # print('done: ', checked)
        # print('to check: ', to_check)
        # print("---")
        current = to_check.pop()
        checked.add(current)
        if garden[current] == symbol:
            garden[current] = "*"
            area.add(current)
            for neighbor in current.neighbors():
                if neighbor.is_inbounds(garden) and not neighbor in checked:
                    to_check.add(neighbor)
            # print(render(garden))
            # print("\n")
    return symbol, area

def find_areas(garden):
    areas = []
    for x, y in [(x, y) for y in range(garden.y_max) for x in range(garden.x_max)]:
        if not garden[x, y] == "*":
            areas.append(flood_fill(garden, Coord(x, y)))
    return areas

def calc_perimeter(area: set[Coord]):
    perimeter = 0
    for cell in area:
        not_in_same_area = cell.neighbors().difference(area)
        perimeter += len(not_in_same_area)
    return perimeter


# for part 2
def find_any_bottom_right_corner(area: set[Coord]):
    for c in area:
        if c + (1, 0) not in area and c + (0, 1) not in area:
            return c

def calc_perimeter_with_lines(area: set[Coord], garden: Garden):
    # for c in area:  # DEBUG
    #     garden[c] = " " # D
    border_groups = group_by_border_direction(area)
    number_of_sides = 0
    for border_group in border_groups.values():
        # for b in border_group: # D
        #     garden[b] = "-" # D
        # print(d) # D
        # print(render(garden)) # D
        # for c in area: # D
        #     garden[c] = " " # D
        line_number = len(create_lines_from_group_by_are_adjacent(border_group))
        number_of_sides += line_number
        # print(line_number) # D
    return number_of_sides

def group_by_border_direction(area: set[Coord]):
    border_groups = {n: set() for n in Coord.directions}
    for c in area:
        for direction in c.directions:
            if c+direction not in area:
                border_groups[direction].add(c)
    return border_groups

def touches_line(line: list[Coord], cell):
    for n in cell.neighbors():
        if n in line:
            return True
    return False

def create_lines_from_group_by_are_adjacent(group: set[Coord]):
    lines = list()
    for c in group:
        add_to_line = None
        merge_lines = None
        for line in lines:
            if touches_line(line, c):
                # cell could merge to existing lines together if they first were disjunct but know connected through this cell
                if add_to_line:
                    merge_lines = add_to_line, line
                else:
                    add_to_line = line
        if merge_lines:
            line1, line2 = merge_lines
            lines.remove(line1)
            lines.remove(line2)
            lines.append(line1 + line2)
        elif add_to_line:
            add_to_line.append(c)
        else:
            lines.append([c])
    return lines


def fence_price(area: set[Coord], perimeter_count: int):
    return len(area) * perimeter_count

def run(file="input.txt"):
    garden = parse(read(file))
    # print(render(garden))
    return sum([fence_price(area, calc_perimeter(area)) for _, area in find_areas(garden)])

def run2(file="input.txt"):
    garden = parse(read(file))
    # print(render(garden))
    total_price = 0
    for sym, area in find_areas(garden):
        perimeter = calc_perimeter_with_lines(area, garden)
        price =  fence_price(area, perimeter)
        total_price += price
        # print(sym, len(area), "*", perimeter, "=", price)
    return total_price
    # return sum([fence_price(area) for _, area in ])


if __name__ == "__main__":
    print(run2("example.txt"))
    print(run2())
