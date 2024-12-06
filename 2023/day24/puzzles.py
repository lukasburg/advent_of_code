import itertools
import re
from math import sqrt

import numpy as np

with open("input") as file:
    inp = file.readlines()


# is a, b:  f(x) = ax + b
Function = tuple[float, float]
ComplexFunction = tuple[complex, complex]


def parse_line(line):
    x, y, z, vx, vy, vz = re.match("(\\d+), (\\d+), (\\d+) @ (-?\\d+), (-?\\d+), (-?\\d+)", line).groups()
    return int(x), int(y), int(z), int(vx), int(vy), int(vz)


def norm_function(x, y, z, vx, vy, vz) -> Function:
    vy_norm = vy / vx  # for vx=1 how much vy
    y_norm = y - vy_norm*x
    return vy_norm, y_norm


def is_in_future_of_function(x, y, z, vx, vy, vz, intersection_x):
    return (x > intersection_x and vx < 0) or (x < intersection_x and vx > 0)


def intersection(f1: Function, f2: Function):
    # f1(x) = a1x + b1 -> a1x + b1 = a2x + b2
    # b1 - b2 = a2x - a1x ->  b1 - b2 = (a2 - a1)x -> x = (b1 - b2)/(a2-a1)
    try:
        x = (f1[1] - f2[1])/(f2[0] - f1[0])
        y = f1[0]*x + f1[1]
        return x, y
    except ZeroDivisionError:
        return None


def run(input_string, area_start, area_end):
    functions = [parse_line(line) for line in input_string]
    intersections_total = 0
    for f1, f2 in itertools.combinations(functions, 2):
        intersect = intersection(norm_function(*f1), norm_function(*f2))
        if intersect:
            x, y = intersect
            f1_future = is_in_future_of_function(*f1, x)
            f2_future = is_in_future_of_function(*f2, x)
            inside_area = area_start <= x <= area_end and area_start <= y <= area_end
            if f1_future and f2_future and inside_area:
                intersections_total += 1
            # future_str = "" if f1_future and f2_future \
            #     else f" ({1 if not f1_future else ''}{2 if not f2_future else ''})"
            # print(f"{f1}, {f2}, intersect {'inside' if inside_area else 'OUTSIDE'} "
            #       f"{'' if f1_future and f2_future else 'NOT '}in future{future_str} at x:{x} y:{y}")
            # print(f"{f1_future} {f2_future}")
        # else:
        #     print(f"{f1}, {f2} are parallel")
    return intersections_total, functions


# Part two
class PointDirectionFunction:
    def __init__(self, function):
        self.start_point = np.array([function[0], function[1], function[2]])
        self.direction = np.array([function[3], function[4], function[5]])


# def normal_abstand(f1: PointDirectionFunction, f2: PointDirectionFunction):
    


def run2(functions):
    functions = [PointDirectionFunction(f) for f in functions]


if __name__ == "__main__":
    intersections, fs = run(inp, 200000000000000, 400000000000000)
    run2(fs)
    # print(run(inp, 7, 27))
