import itertools
import re


with open("input") as file:
    inp = file.readlines()


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'P(x={self.x}, y={self.y})'

    def __repr__(self):
        return str(self)


class Circle:
    def __init__(self, middle: Point, radius: int):
        self.middle = middle
        self.radius = radius

    def __str__(self):
        return f'C({self.middle}, {self.radius})'

    def __repr__(self):
        return str(self)


coordinate_matcher = re.compile('[\w ]*=(-?\d+)\D+(-?\d+):[\w ]*=(-?\d+)\D+(-?\d+)')
PointSet = set[Point]
CircleSet = set[Circle]


def parse(string):
    sx, sy, bx, by = coordinate_matcher.search(string).groups()
    return Point(int(sx), int(sy)), Point(int(bx), int(by))


def start_end(a_list):
    return a_list[0], a_list[-1]


def format_grid(sensors: PointSet, beacons: PointSet, cover: CircleSet):
    points = sensors.union(beacons)
    x_min, x_max = start_end(sorted([p.x for p in points]))
    y_min, y_max = start_end(sorted([p.y for p in points]))
    width_padding = ''.join([' ' for i in range(x_min-1, x_max-2)])
    total_str = [f'   {x_min}{width_padding}{x_max}', f'    v{width_padding}v']
    for y in range(y_min, y_max+1):
        formatted_x = ['S' if Point(p, y) in sensors else 'B' if Point(p, y) in beacons else
                       '#' if is_in_circles(Point(p, y), cover) else '.'
                       for p in range(x_min, x_max+1)]
        total_str.append(f'{y:3} {"".join(formatted_x)}')
    return '\n'.join(total_str)


def manhattan_distance(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)


def is_in_circles(p: Point, cs: CircleSet):
    for c in cs:
        if manhattan_distance(c.middle, p) <= c.radius:
            return True
    return False


sensors, beacons, circles = set(), set(), set()
xmin = 0
xmax = 0
for line in inp:
    sensor, beacon = parse(line)
    sensors.add(sensor)
    beacons.add(beacon)
    distance_sensor_beacon = manhattan_distance(sensor, beacon)
    new_xmin = sensor.x - distance_sensor_beacon - 1
    new_xmax = sensor.x + distance_sensor_beacon
    xmin = new_xmin if new_xmin < xmin else xmin
    xmax = new_xmax if new_xmax > xmax else xmax
    circles.add(Circle(sensor, distance_sensor_beacon))


# look_at_line = 10
look_at_line = 2000000


def covered_but_not_object(p: Point, cs: CircleSet):
    return p not in beacons and is_in_circles(p, cs)


def filter_irrelevant_circles(cs: CircleSet, respective_to_y):
    relevant_circles = set()
    for c in cs:
        point_inline = Point(c.middle.x, respective_to_y)
        if manhattan_distance(c.middle, point_inline) <= c.radius:
            relevant_circles.add(c)
    return relevant_circles


# print(circles)
covering_line_to_look_at = filter_irrelevant_circles(circles, look_at_line)
# print(covering_line_to_look_at)

# Solution part 1, takes a lot of time to compute
# print(len(list(filter(lambda k: covered_but_not_object(Point(k, look_at_line), covering_line_to_look_at), range(xmin, xmax + 1)))))

#
# ======
# Part 2
# ======
#

## Explanation:
# We look for a point, that is not covered by any beacon
# There is only 1 such point
# This 1 point must lie on a line between two circles, that leave just a single space between them
# See grafik in this dir

# print(f'Number of cirlces = {len(circles)}, comparing all to all {sum(range(len(circles)))}')
circles_as_list = list(circles)
candidates = set()
for i, c1 in enumerate(circles_as_list):
    for c2 in circles_as_list[i+1:]:
        if manhattan_distance(c1.middle, c2.middle) == c1.radius + c2.radius + 2:
            candidates.add((c1, c2))
# print(candidates)


class DiagonalLine:
    def __init__(self, start_x, slope):
        self.start_x = start_x
        self.slope = slope

    def __str__(self):
        return f'L(x={self.start_x}, slope={self.slope})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.start_x == other.start_x and self.slope == other.slope

    def __hash__(self):
        return hash((self.start_x, self.slope))


def construct_line(c1: Circle, c2: Circle):
    left_circle, right_circle = (c1, c2) if c1.middle.x < c2.middle.x else (c2, c1)
    slope = 1 if left_circle.middle.y > right_circle.middle.y else -1
    point_on_line_between = Point(left_circle.middle.x + left_circle.radius + 1, left_circle.middle.y)
    print(point_on_line_between)
    start_point = point_on_line_between.y - (point_on_line_between.x*slope)
    print(start_point, slope)
    return DiagonalLine(start_point, slope)


def find_intersection(line1: DiagonalLine, line2: DiagonalLine):
    y = (line1.start_x + line2.start_x) // 2
    # half the distance between the two point they meet.
    x = abs(line1.start_x - line2.start_x)//2
    return Point(x, y)


def point_on_line(line: DiagonalLine, point: Point):
    return (point.x * line.slope) + line.start_x == point.y


def point_on_lines(lines: set[DiagonalLine], point: Point):
    for line in lines:
        if point_on_line(line, point):
            return True
    return False


def format_lines(x_min, x_max, y_min, y_max, lines):
    total_str = []
    for y in range(y_min,y_max):
        total_str.append(f'{y:2} ' +
            ''.join(['x' if point_on_lines(lines,Point(x, y)) else '.'
                     for x in range(x_min, x_max)])
        )
    return '\n'.join(total_str)


# Luckily in my input only two possible lines turned up.
# Point must be on intersection of thesepermutations two
# print(format_grid(sensors, beacons, circles))
lines = set(construct_line(c1, c2) for c1, c2 in candidates)
# print(format_lines(0, 30, -10, 30, lines))
print(lines)

for a, b in itertools.permutations(lines, 2):
    intersection = find_intersection(a, b)
    print(f'Verification: is {intersection} in circles? {is_in_circles(intersection, circles)}')
    solution = intersection.x * 4000000 + intersection.y
    if solution == 56000023:
        print(a, b)
    print(f'Solution part 2 {solution}, intersection: {intersection}')
