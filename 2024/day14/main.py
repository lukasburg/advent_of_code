import re
import time
from collections import defaultdict
from functools import reduce
from operator import mul
from itertools import product
from PIL import Image
import numpy
import progressbar
from offset_smallest_common_denominator import alignment
# import scipy.misc as smp


class Bot:
    def __init__(self, start_x, start_y, v_x, v_y):
        self.pos = complex(start_x, start_y)
        self.v = complex(v_x, v_y)

    def __str__(self):
        return f"B({self.pos}, +{self.v})"

    def position_after(self, time, map_size):
        pos = self.pos + time * self.v
        return complex(pos.real % map_size.real, pos.imag % map_size.imag)

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string) -> list[Bot]:
    return [Bot(*map(int, re.findall('-?\\d+', line))) for line in string.split("\n")]

def in_quadrant(pos, map_size):
    if pos.real == map_size.real // 2 or pos.imag == map_size.imag // 2:
        return 0
    x_part = 1 if pos.real < (map_size.real // 2) else 2
    y_part = 0 if pos.imag < (map_size.imag // 2) else 2
    return x_part+y_part

def in_square(pos, map_size, square_count):
    x = (pos.real * square_count) // map_size.real
    y = (pos.imag * square_count) // map_size.imag
    return x, y

def render(bot_positions, map_size, sym=None):
    return "\n".join(["".join([
        (sym if sym else str(bot_positions[complex(x, y)])) if bot_positions[complex(x, y)] else '.'
        for x in range(int(map_size.real))])
        for y in range(int(map_size.imag))])

def create_big_array(map_size, times):
    x_len, y_len = int(map_size.real*times+times), int(map_size.imag*times+times)
    return numpy.zeros((y_len, x_len, 3), dtype=numpy.uint8)

def fill_array(array, bot_positions, map_size, offset_x, offset_y):
    # as_list = [[255 if bot_position[complex(x, y)] else 0 for x in range(int(map_size.real))] for y in range(int(map_size.imag))]
    x_len, y_len = int(map_size.real), int(map_size.imag)
    for pos in bot_positions:
        array[int(pos.imag)+offset_y*y_len+offset_y, int(pos.real)+offset_x*x_len+offset_x] = [255, 0, 0]
    # for x, y in product(range(x_len), range(y_len)):
    #     array[y+offset_y*y_len+offset_y, x+offset_x*x_len+offset_x] = \
    #         [255, 255, 255] if complex(x, y) in bot_positions else [0,0,0]

def offset_calc(offset, times):
    return offset%times, offset//times

def safe_big_array_as_image(a):
    img = Image.fromarray(a)
    # img = img.convert('RGB')
    # img.show()
    img.save('out.png')

def quadrant_product(count_per_quadrant):
    return reduce(mul, [count_per_quadrant[i] for i in range(1, 5)], 1)

def run(file="input.txt", map_size=101+103j):
    # print(in_quadrant((6+0j), map_size))
    bots = parse(read(file))
    count_per_quadrant = {i: 0 for i in range(5)}
    # all_positions = defaultdict(lambda: 0)
    for i, bot in enumerate(bots):
        final_pos = bot.position_after(100, map_size)
        # all_positions[final_pos] += 1
        # print(final_pos, in_quadrant(final_pos, map_size))
        count_per_quadrant[in_quadrant(final_pos, map_size)] += 1
        # print(i, bot, final_pos, in_quadrant(final_pos, map_size))
    # print(render(all_positions, map_size))
    print(quadrant_product(count_per_quadrant))

def relative_difference(v1, v2):
    return 0.9 <= v1/v2 <= 1.1

def symmetrical_quadrants(count_per_quadrant, squares):
    for y in range(squares):
        for x in range(squares//2):
            if not relative_difference(count_per_quadrant[x, y], count_per_quadrant[squares-1-x, y]):
                return False
    return True
    # return (relative_difference(count_per_quadrant[1], count_per_quadrant[2])
    #         and relative_difference(count_per_quadrant[3], count_per_quadrant[4])
    #         and count_per_quadrant[1] < count_per_quadrant[3]
    #         and count_per_quadrant[2] < count_per_quadrant[4])

def safe_as_img(bot_positions, map_size, n):
    x_len, y_len = int(map_size.real), int(map_size.imag)
    a = numpy.full((y_len, x_len, 3), [0, 0, 0], dtype=numpy.uint8)
    for pos in bot_positions:
        a[int(pos.imag), int(pos.real)] = [255, 0, 0]
    img = Image.fromarray(a)
    img.save(f'images/out{n}.png')

def render_at_time(bots, time, map_size):
    all_positions = set()
    for bot in bots:
        pos = bot.position_after(time, map_size)
        # count_per_quadrant[in_square(pos, map_size, square_count)] += 1
        all_positions.add(pos)
        # fill_array(a, all_positions, map_size, *offset_calc(t, times))
    safe_as_img(all_positions, map_size, time)

def easter_egg(file="input.txt", map_size=101+103j):
    bots = parse(read(file))
    times = 100
    a = create_big_array(map_size, times)
    with progressbar.ProgressBar(max_value=times*times, redirect_stdout=True) as bar:
        for t in range(times*times):
            bar.update(t)
            all_positions = defaultdict(lambda: 0)
            for bot in bots:
                all_positions[bot.position_after(t, map_size)] += 1
            fill_array(a, all_positions, map_size, *offset_calc(t, times))
        # render_at_time(bots, t, map_size)
    safe_big_array_as_image(a)


def render_at_aligned_time(file="input.txt", map_size=101+103j):
    # spotted by looking at output
    horizontals = 60, 163
    verticals = 83, 184
    v_h_aligned = alignment(horizontals[1] - horizontals[0], horizontals[1], verticals[1] - verticals[0], verticals[1])
    bots = parse(read(file))
    render_at_time(bots, v_h_aligned, map_size)
    # safe_big_array_as_image(a)

if __name__ == "__main__":
    render_at_aligned_time()
    # print(alignment(horizontals[1] - horizontals[0], horizontals[1]))
    run("example.txt", 11+7j)
    # easter_egg("example.txt", 11+7j)
    run()
    easter_egg()
