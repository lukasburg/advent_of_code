with open("input") as file:
    inp = file.readlines()

grid = [[int(i) for i in line.strip()] for line in inp]
width = len(grid[0])
heigth = len(grid[0])
visibles = set()


def visible_in_line(line):
    visible_this_line = set()
    current_max_heigth = -1
    for i, tree in enumerate(line):
        if tree > current_max_heigth:
            current_max_heigth = tree
            visible_this_line.add(i)
    return visible_this_line


for x, row in enumerate(grid):
    visible_here = {(x, y) for y in visible_in_line(row)}
    visible_here = visible_here.union({(x, width-y-1) for y in visible_in_line(reversed(row))})
    visibles = visibles.union(visible_here)
    # print(row, visible_here)

print("---")

for y, column in enumerate([[grid[j][i] for j in range(heigth)] for i in range(width)]):
    visible_here = {(x, y) for x in visible_in_line(column)}
    visible_here = visible_here.union({(heigth-x-1, y) for x in visible_in_line(reversed(column))})
    visibles = visibles.union(visible_here)
    # print(column, visible_here)


print('trees visible from outside the grid:', len(visibles))


def get_view_distance(view, tree_height):
    for i, point in enumerate(view):
        x, y = point[0], point[1]
        if grid[x][y] >= tree_height:
            return i+1
    else:
        return len(view)


# scenic scores.
# Ignore trees at border, one direction will always be 0, and score is multiplied
current_high_score = 0
for x, y in [(x, y) for y in range(1, width-1) for x in range(1, heigth-1)]:
    current_tree = grid[x][y]
    left = [(x, new_y) for new_y in range(0, y)[::-1]]
    right = [(x, new_y) for new_y in range(y+1, heigth)]
    up = [(new_x, y) for new_x in range(0, x)[::-1]]
    down = [(new_x, y) for new_x in range(x+1, width)]
    view_l = get_view_distance(left, current_tree)
    view_r = get_view_distance(right, current_tree)
    view_u = get_view_distance(up, current_tree)
    view_d = get_view_distance(down, current_tree)
    score = view_u * view_r * view_d * view_l
    current_high_score = score if score > current_high_score else current_high_score
    # print(f"{x, y}; u:{view_u}, r: {view_r}, d: {view_d}, l: {view_l}, s: {score}")
    # print()

print('highest scenic score: ', current_high_score)