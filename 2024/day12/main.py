import itertools
from copy import copy

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    return Garden([[cell for cell in line] for line in string.split("\n")])

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}|{self.y})"

    def neighbors(self):
        return {Coord(self.x, self.y-1), Coord(self.x, self.y+1), Coord(self.x-1, self.y), Coord(self.x+1, self.y)}

    def is_inbounds(self, garden: "Garden"):
        return 0 <= self.x < garden.x_max and 0 <= self.y < garden.y_max

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

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

def fence_price(area: set[Coord]):
    return len(area) * calc_perimeter(area)

def run(file="input.txt"):
    garden = parse(read(file))
    # print(render(garden))
    return sum([fence_price(area) for _, area in find_areas(garden)])

if __name__ == "__main__":
    print(run("example.txt"))
    print(run())
