import re

with open('input') as file:
    inp = file.readlines()


Point = tuple[int, int]
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


class SandFallingTrough(Exception):
    pass


class Grid:
    sand_sym = f'{WARNING}o{ENDC}'
    falls_sym = f'{FAIL}~{ENDC}'

    def __init__(self):
        self.rock: set[Point] = set()
        self.sand: set[Point] = set()
        self.x_min = 100000000
        self.x_max = 0
        self.y_max = 0
        self.sand_spawn = (500, 0)
        self.falls_through_point = None

    def __contains__(self, item: Point):
        return item in self.rock or item in self.sand

    def add_rock(self, rock: Point):
        self.x_min = rock[0] if self.x_min > rock[0] else self.x_min
        self.x_max = rock[0] if self.x_max < rock[0] else self.x_max
        self.y_max = rock[1] if self.y_max < rock[1] else self.y_max
        self.rock.add(rock)

    def move_sand_down(self, sand: Point):
        sand_x, sand_y = sand
        if (sand_x, sand_y+1) not in self:  # space below is empty
            return sand_x, sand_y + 1  # go further down
        elif (sand_x-1, sand_y+1) not in self:  # space left below is empty
            return sand_x - 1, sand_y + 1
        elif (sand_x+1, sand_y+1) not in self:  # space right below is empty
            return sand_x + 1, sand_y + 1
        return sand_x, sand_y

    def add_sand(self, sand: Point):
        self.x_min = sand[0] if self.x_min > sand[0] else self.x_min
        self.x_max = sand[0] if self.x_max < sand[0] else self.x_max
        self.sand.add(sand)

    def spawn_sand(self):
        new_sand_x, new_sand_y = self.sand_spawn
        while new_sand_y < self.y_max and self.x_min < new_sand_x < self.x_max:
            new_sand_x, next_y = self.move_sand_down((new_sand_x, new_sand_y))
            if new_sand_y == next_y:
                self.add_sand((new_sand_x, new_sand_y))
                return True
            new_sand_y = next_y
        self.falls_through_point = (new_sand_x, new_sand_y)
        return False

    def format(self):
        width_padding = ''.join([' ' for i in range(self.x_min-1, self.x_max-2)])
        total_str = [f'    {self.x_min//100}{width_padding}{self.x_max//100}',
                     f'    {(self.x_min%100)//10}{width_padding}{(self.x_max%100)//10}',
                     f'    {self.x_min%10}{width_padding}{self.x_max%10}']
        for y in range(self.y_max+1):
            points = ['#' if (p, y) in self.rock else self.sand_sym if (p, y) in self.sand else
                      self.falls_sym if (p, y) == self.falls_through_point else '.'
                      for p in range(self.x_min, self.x_max+1)]
            total_str.append(f'{y:3} {"".join(points)}')
        return '\n'.join(total_str)


class GridWithBottom(Grid):
    def format(self):
        self.y_max = self.y_max + 1  # temporarily lower floor for correct printing, bit of a hack
        floor = f'\nF:  {"".join(["#" for i in range(self.x_min, self.x_max+1)])}'
        format_string = super().format() + floor
        self.y_max = self.y_max - 1
        return format_string

    def __contains__(self, item):
        return super().__contains__(item) or item[1] == self.y_max + 2

    def spawn_sand(self):
        new_sand_x, new_sand_y = self.sand_spawn
        while self.sand_spawn not in self.sand:
            new_sand_x, next_y = self.move_sand_down((new_sand_x, new_sand_y))
            if new_sand_y == next_y:
                self.add_sand((new_sand_x, new_sand_y))
                return True
            new_sand_y = next_y
        return False


def abs_range(start, end):
    return range(start, end+1) if start < end else reversed(range(end, start+1))


def parse_inp():
    number_matcher = re.compile('(\d+),(\d+)')
    points_to_add = set()
    for line in inp:
        points = [(int(x_str), int(y_str)) for x_str, y_str in number_matcher.findall(line)]
        cx, cy = points[0]
        for x, y in points[1:]:
            if x != cx:
                points_between_current_and_new = {(x_new, y) for x_new in abs_range(cx, x)}
            elif y != cy:
                points_between_current_and_new = {(x, y_new) for y_new in abs_range(cy, y)}
            points_to_add = points_to_add.union(points_between_current_and_new)
            cx, cy = x, y
    return points_to_add


rocks = parse_inp()

grid = Grid()
for rock in rocks:
    grid.add_rock(rock)

while grid.spawn_sand():
    pass
print(grid.format())
print(f'Grid contains {len(grid.sand)} sand')


grid_with_bottom = GridWithBottom()
for rock in rocks:
    grid_with_bottom.add_rock(rock)

while grid_with_bottom.spawn_sand():
    pass
    # print(grid_with_bottom.format())
print(grid_with_bottom.format())
print(f'Grid contains {len(grid_with_bottom.sand)} sand')
