import itertools
import re
from pprint import pprint

with open("input") as file:
    inp = file.readlines()


class Galaxy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise KeyError(item)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def render(image):
    for row in image:
        print(''.join(row))


def expand_space(image):
    new_rows = []
    for row in image:
        row = row[:-1]
        new_rows.append(row)
        if re.fullmatch('[.]*', row):
            # double if empty
            new_rows.append(row)
    new_cols = []
    for col in [[new_rows[y][x] for y in range(len(new_rows))] for x in range(len(new_rows[0]))]:
        new_cols.append(col)
        if re.fullmatch('[.]*', ''.join(col)):
            # double if empty
            new_cols.append(col)
    padded_image = [[new_cols[y][x] for y in range(len(new_cols))] for x in range(len(new_cols[0]))]
    return padded_image


expanded_image = expand_space(inp)
galaxies = set()
for y, row in enumerate(expanded_image):
    for x, symbol in enumerate(row):
        if symbol == '#':
            galaxies.add((x, y))


def get_distance(pair):
    return abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])


def calc_total_dist(galaxies):
    return sum(map(get_distance, itertools.combinations(galaxies, 2)))


total_distance = calc_total_dist(galaxies)
print(f"Total distances: {total_distance}")


# PART TWO


def better_expanded_galaxies(image, factor):
    adjusted_factor = factor-1
    galaxies = set()
    track_amount_empty_rows = 0
    track_empty_cols = list(range(len(image[0])))
    for y, row in enumerate(image):
        row = row[:-1]
        if re.fullmatch('[.]*', row):
            track_amount_empty_rows += 1
        for x, symbol in enumerate(row):
            if symbol == "#":
                galaxies.add(Galaxy(x, y+adjusted_factor*track_amount_empty_rows))
                if x in track_empty_cols:
                    track_empty_cols.remove(x)
    for galaxy in galaxies:
        cols_before = len(list(filter(lambda c: c < galaxy.x, track_empty_cols)))
        galaxy.x += cols_before*adjusted_factor
    return galaxies


second_galaxies = better_expanded_galaxies(inp, 1000000)
print(f"Total distances: {calc_total_dist(second_galaxies)}")
