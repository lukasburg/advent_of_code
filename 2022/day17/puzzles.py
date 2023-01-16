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


ROCKS_IN_ORDER = [  # start with leftmost point with a distance of 2 to the left wall
    ({2+0j, 3+0j, 4+0j, 5+0j}, '-'),  # 1. Line (-)
    ({2+1j, 3+0j, 3+1j, 3+2j, 4+1j}, '+'),  # 2. Plus (+)
    ({2+0j, 3+0j, 4+0j, 4+1j, 4+2j}, 'L'),  # 3. Reverse L (J)
    ({2+0j, 2+1j, 2+2j, 2+3j}, 'I'),  # 4. Line (I)
    ({2+0j, 2+1j, 3+0j, 3+1j}, '#'), # 5. Square (#)
]


def direction_generator(direction_str):
    while True:
        for direction in direction_str:
            yield 1 if direction == '>' else -1


def shape_generator(length):
    i = 0
    while i < length:
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


def main(rock_count, direction_str):
    directions_iter = direction_generator(direction_str)
    current_height = 3
    rock_points = set()
    for shape, name in shape_generator(rock_count):
        rock = Rock(shape, complex(0, current_height), name=name)
        could_move_down = True
        while could_move_down:
            rock.try_move_sideways(next(directions_iter), rock_points)
            could_move_down = rock.try_move_down(rock_points)  # move down, loop exits, if that was not possible
        rock_points.update(rock.points)
        rock_highest_point = rock.get_max_height()
        current_height = current_height if rock_highest_point + 4 <= current_height else rock_highest_point + 4
    return current_height - 3


ROCK_COUNT = 2022
with open('example_input') as file:
    inp = file.read().strip()


print('Tower height: ', main(ROCK_COUNT, inp))
