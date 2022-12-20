from collections import defaultdict
from itertools import chain
from pprint import pprint

with open('input') as file:
    inp = file.readlines()


def parse_input(string: str):
    x, y, z = [int(i) for i in string.strip().split(',')]
    return x, y, z


class NonUpdatingDefaultDict(defaultdict):
    def __missing__(self, key):
        return self.default_factory()


Coords = dict[int, dict[int, dict[int, bool]]]
Point = tuple[int, int, int]


def create_coords(lines):
    coords = defaultdict(lambda: defaultdict(lambda: NonUpdatingDefaultDict(lambda: False)))
    true_coords = set()
    for line in lines:
        x, y, z = parse_input(line)
        coords[x][y][z] = True
        true_coords.add((x, y, z))
    return coords, true_coords


def get_neighbors(x, y, z):
    return [
        (x-1, y, z), (x+1, y, z),
        (x, y-1, z), (x, y+1, z),
        (x, y, z-1), (x, y, z+1)
    ]


def point_in_coords(x, y, z, coords: Coords):
    return coords[x][y][z]


def calculate_surface_area(coords: Coords, true_coords: set[Point]):
    surface_area = 0
    for point in true_coords:
        neighbors = get_neighbors(*point)
        surface_area += len(list(filter(lambda n: not point_in_coords(*n, coords), neighbors)))
    return surface_area


def find_bounds(coords: Coords):
    all_x = sorted(coords.keys())
    x_min, x_max = all_x[0], all_x[-1]
    all_y = sorted(chain(*[y.keys() for y in coords.values()]))
    y_min, y_max = all_y[0], all_y[-1]
    all_z = sorted(chain(*[chain(*[z.keys() for z in y.values()]) for y in coords.values()]))
    z_min, z_max = all_z[0], all_z[-1]
    return (x_min-1, x_max+1), (y_min-1, y_max+1), (z_min-1, z_max+1)


def point_inside_max(x, y, z, x_bounds, y_bounds, z_bounds):
    return (x_bounds[0] <= x <= x_bounds[1]
            and y_bounds[0] <= y <= y_bounds[1]
            and z_bounds[0] <= z <= z_bounds[1])


def find_outside_surface_area(coords: Coords):
    bounds = find_bounds(coords)
    start_point = (bounds[0][0], bounds[1][0], bounds[2][0])
    outside = [start_point]
    surface_area = 0
    i = 0
    while len(outside) > i:
        next_point = outside[i]
        i += 1
        neighbors = get_neighbors(*next_point)
        for neighbor in neighbors:
            if point_in_coords(*neighbor, coords):
                surface_area += 1
            elif point_inside_max(*neighbor, *bounds) and neighbor not in outside:
                outside.append(neighbor)
        # print(f'remaining points {len(outside)}, visited {i}')
    return surface_area


def main():
    coords, true_coords = create_coords(inp)
    print(calculate_surface_area(coords, true_coords))
    print(find_outside_surface_area(coords))


main()
