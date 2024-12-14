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

def calc_perimeter_with_lines(area: set[Coord], garden):
    for c in area:
        garden[c] = " "
    current_corner = find_any_bottom_right_corner(area)
    garden[current_corner] = "C"
    been_on = set()
    direction_iterator = ClockwiseIterator()
    direction, outwards = next(direction_iterator)
    # garden[start_corner + outwards] = "#"
    # garden[start_corner + direction] = "Q"

    print(render(garden))

def fence_price(area: set[Coord]):
    return len(area) * calc_perimeter(area)

def run(file="input.txt"):
    garden = parse(read(file))
    # print(render(garden))
    return sum([fence_price(area) for _, area in find_areas(garden)])

def run2(file="input.txt"):
    garden = parse(read(file))
    # print(render(garden))
    for _, area in find_areas(garden):
        calc_perimeter_with_lines(area, garden)
        break
    # return sum([fence_price(area) for _, area in ])


if __name__ == "__main__":
    print(run2("example.txt"))
    # print(run())
