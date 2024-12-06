import re
from functools import reduce
from math import sqrt
from operator import mul

with open("input") as file:
    inp = file.readlines()


def find_min_max(time, record):
    sq_root = sqrt(
        pow(time, 2) / 4 - record
    )
    maximum = int(time/2 + sq_root) if not sq_root.is_integer() else int(time/2 + sq_root) - 1
    minimum = int(time/2 - sq_root) + 1
    return minimum, maximum


def margin_of_error(minimum, maximum):
    return maximum - minimum + 1


times, records = ([int(number) for number in re.findall('\\d+', line)] for line in inp)
races = [(times[i], records[i]) for i in range(len(times))]
ways_to_win = [margin_of_error(*find_min_max(time, record)) for time, record in races]
print(f"Product of margins of error {reduce(mul, ways_to_win)}")


time, record = (int(''.join(c for c in line if c.isdigit())) for line in inp)
print(f"Margin of error in single long race: {margin_of_error(*find_min_max(time, record))}")
