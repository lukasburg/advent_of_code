from collections import defaultdict

with open("input") as file:
    inp = file.readlines()


lines = [tuple([tuple([int(coord) for coord in point.split(',')]) for point in line.split(' -> ')]) for line in inp]
straight_lines = list(filter(lambda p: p[0][0] == p[1][0] or p[0][1] == p[1][1], lines))


def abs_range(start, end):
    return range(start, end+1) if start < end else reversed(range(end, start+1))


point_dict = defaultdict(lambda: 0)
# for line in straight_lines:
for line in lines:
    if line[0][0] == line[1][0]:  # horizontal
        points = [(line[0][0], i) for i in abs_range(line[0][1], line[1][1])]
    elif line[0][1] == line[1][1]:  # vertical
        points = [(i, line[0][1]) for i in abs_range(line[0][0], line[1][0])]
    else:
        points = [(x, y) for x, y in zip(abs_range(line[0][0], line[1][0]), abs_range(line[0][1], line[1][1]))]
    for point in points:
        point_dict[point] += 1


# print(point_dict.values())
print(len([i for i in point_dict.values() if i > 1]))

# grid = '   123456789\n'
# for i in range(1000):
#     row = f'{i}: '
#     for j in range(1000):
#         row += str(point_dict[(j, i)]) if point_dict[(j, i)] != 0 else '.'
#     grid += row + '\n'
# print(grid)
