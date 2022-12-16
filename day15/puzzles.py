import re
from datetime import datetime


with open("input") as file:
    inp = file.readlines()

coordinate_matcher = re.compile('[\w ]*=(-?\d+)\D+(-?\d+):[\w ]*=(-?\d+)\D+(-?\d+)')
Point = tuple[int, int]
Circle = tuple[Point, int]
PointSet = set[Point]
CircleSet = set[Circle]


def parse(string):
    sx, sy, bx, by = coordinate_matcher.search(string).groups()
    return (int(sx), int(sy)), (int(bx), int(by))


def start_end(a_list):
    return a_list[0], a_list[-1]


def format_grid(sensors: PointSet, beacons: PointSet, cover: CircleSet):
    points = sensors.union(beacons)
    x_min, x_max = start_end(sorted([x for x, _ in points]))
    y_min, y_max = start_end(sorted([y for _, y in points]))
    width_padding = ''.join([' ' for i in range(x_min-1, x_max-2)])
    total_str = [f'   {x_min}{width_padding}{x_max}', f'    v{width_padding}v']
    for y in range(y_min, y_max+1):
        formatted_x = ['S' if (p, y) in sensors else 'B' if (p, y) in beacons else
                       '#' if is_in_circles((p, y), cover) else '.'
                       for p in range(x_min, x_max+1)]
        total_str.append(f'{y:3} {"".join(formatted_x)}')
    return '\n'.join(total_str)


def manhattan_distance(a: Point, b: Point):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def draw_manhattan_circle(middle_point: Point, radius: int):
    area = set()
    for x in range(middle_point[0]-radius, middle_point[0]+radius+1):
        distance_x_middle = abs(middle_point[0]-x)
        for y in range(middle_point[1]-radius+distance_x_middle, middle_point[1]+radius-distance_x_middle+1):
            area.add((x, y))
    return area


def is_in_circles(p: Point, cs: CircleSet):
    for circle_middlepoint, radius in cs:
        if manhattan_distance(circle_middlepoint, p) <= radius:
            return True
    return False


sensors, beacons, covered = set(), set(), set()
xmin = 0
xmax = 0
for line in inp:
    sensor, beacon = parse(line)
    sensors.add(sensor)
    beacons.add(beacon)
    distance_sensor_beacon = manhattan_distance(sensor, beacon)
    new_xmin = sensor[0] - distance_sensor_beacon - 1
    new_xmax = sensor[0] + distance_sensor_beacon
    xmin = new_xmin if new_xmin < xmin else xmin
    xmax = new_xmax if new_xmax > xmax else xmax
    covered.add((sensor, distance_sensor_beacon))


look_at_line = 2000000


def covered_but_not_object(p, cs):
    return p not in beacons and is_in_circles(p, cs)


def filter_irrelevant_circles(cs: CircleSet, respective_to_y):
    relevant_circles = set()
    for circle_middlepoint, radius in cs:
        circle_x = circle_middlepoint[0]
        point_inline = (circle_x, respective_to_y)
        if manhattan_distance(circle_middlepoint, point_inline) <= radius:
            relevant_circles.add((circle_middlepoint, radius))
    return relevant_circles


print(covered)
covered = filter_irrelevant_circles(covered, look_at_line)
print(covered)

print(len(list(filter(lambda k: covered_but_not_object((k, look_at_line), covered), range(xmin, xmax + 1)))))
