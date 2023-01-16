class Rock:
    def __init__(self, points: set[complex], start_height, name: str):
        self.points = set(map(lambda i: i+start_height, points))
        self.name = name

    def _move(self, direction: complex):
        return {point+direction for point in self.points}

    def try_move_sideways(self, direction, other_points):
        new_points = self._move(direction)  # try to move to next side
        if not (new_points.intersection(other_points) or self.are_out_of_side_bounds(new_points)):
            self.points = new_points

    def try_move_down(self, other_points):
        new_points = self._move(-1j)
        if not new_points.intersection(other_points) and not self.are_below_ground(new_points):
            self.points = new_points
            return True
        return False

    @classmethod
    def are_out_of_side_bounds(cls, points):
        x_set = {point.real for point in points}
        return -1 in x_set or 7 in x_set

    @classmethod
    def are_below_ground(self, points):
        return -1 in {point.imag for point in points}

    def get_max_height(self):
        return int(max(self.points, key=lambda i: i.imag).imag)

    def __repr__(self):
        return str(self.points)


class DirGeneratorAndRegularityFinder:
    def __init__(self, direction_str):
        self.direction_str = direction_str
        self.generator = direction_generator(direction_str)
        self.previous_height = 0
        self.previous_rock_number = 0
        self.reihe = []

    def next(self, current_height, rock, rock_number):
        try:
            return next(self.generator)
        except StopIteration:
            self.generator = direction_generator(self.direction_str)
            height_diff = current_height - self.previous_height
            rock_diff = rock_number - self.previous_rock_number
            print('=== Directions restarting ===')
            print(f'Current height: {current_height} {height_diff:+}, rock {rock_number} {rock_diff:+}: {rock.name}')
            self.previous_height = current_height
            self.previous_rock_number = rock_number
            self.reihe.append((height_diff, rock_diff))
            return next(self.generator)

    def has_found_regularity(self):
        return len(self.reihe[-3:]) >= 3 and len(set(self.reihe[-3:])) == 1

    def regularity(self):
        return self.reihe[-1]


ROCKS_IN_ORDER = [  # start with leftmost point with a distance of 2 to the left wall
    ({2+0j, 3+0j, 4+0j, 5+0j}, '-'),  # 1. Line (-)
    ({2+1j, 3+0j, 3+1j, 3+2j, 4+1j}, '+'),  # 2. Plus (+)
    ({2+0j, 3+0j, 4+0j, 4+1j, 4+2j}, 'L'),  # 3. Reverse L (J)
    ({2+0j, 2+1j, 2+2j, 2+3j}, 'I'),  # 4. Line (I)
    ({2+0j, 2+1j, 3+0j, 3+1j}, '#'),  # 5. Square (#)
]


def direction_generator(direction_str):
    for direction in direction_str:
        yield 1 if direction == '>' else -1


def shape_generator():
    i = 0
    while True:
        yield ROCKS_IN_ORDER[i % len(ROCKS_IN_ORDER)]
        i += 1


def format_map(rock_points: set[complex], max_height, current_rock: Rock = None):
    all_lines = ['+-------+']
    for y in range(0, max_height+1):
        line = ''.join(['#' if complex(x, y) in rock_points else
                        '@' if current_rock and complex(x, y) in current_rock.points else
                        '.'
                        for x in range(7)])
        all_lines.append('|' + line + '|')
    return '\n'.join(reversed(all_lines)) + '\n'


def main(direction_str, rock_count):
    directions_generator_and_regularity_finder = DirGeneratorAndRegularityFinder(direction_str)
    current_height = 3
    rock_points = set()
    add_later_set = False
    for i, shape in enumerate(shape_generator()):
        rock = Rock(shape[0], complex(0, current_height), name=shape[1])
        could_move_down = True
        while could_move_down:
            rock.try_move_sideways(directions_generator_and_regularity_finder.next(current_height, rock, i), rock_points)
            could_move_down = rock.try_move_down(rock_points)  # move down, loop exits, if that was not possible
            if directions_generator_and_regularity_finder.has_found_regularity() and not add_later_set:
                missing_rocks = rock_count - i
                height_in_regularity, rock_count_in_regularity = directions_generator_and_regularity_finder.regularity()
                fits_x_times = missing_rocks//rock_count_in_regularity
                run_until_i = (missing_rocks % rock_count_in_regularity) + i - 1
                add_to_height_later = fits_x_times * height_in_regularity
                add_later_set = True
        rock_points.update(rock.points)
        rock_highest_point = rock.get_max_height()
        current_height = current_height if rock_highest_point + 4 <= current_height else rock_highest_point + 4
        if add_later_set and i >= run_until_i:
            break
    return current_height - 3 + add_to_height_later


with open('input') as file:
    inp = file.read().strip()


ROCK_COUNT = 1000000000000
print('Tower height: ', main(inp, ROCK_COUNT))
