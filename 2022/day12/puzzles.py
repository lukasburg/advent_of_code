with open('input') as file:
    inp = file.readlines()


class Node:
    def __init__(self, height, x, y):
        self.height = height
        self.symbol = height
        self.cost = 1000000000
        self.x = x
        self.y = y
        self.path_from = '.'

    def dist_str(self):
        infinity = " \u221E"
        return self.cost if self.cost < 1000000 else infinity

    def __repr__(self):
        return f'(x={self.x}, y={self.y}, h={self.height}, c={self.dist_str()})'


class Queue:
    def __init__(self):
        self.ordered_list: list[Node] = []

    def insert_or_update(self, new_node: Node):
        if new_node in self.ordered_list:
            self.ordered_list.remove(new_node)
        for index, node in enumerate(self.ordered_list):
            if node.cost > new_node.cost:
                self.ordered_list.insert(index, node)
                break
        else:
            self.ordered_list.append(new_node)

    def __str__(self):
        return f'{self.ordered_list}'

    def get_next(self):
        return self.ordered_list.pop(0)

    def __bool__(self):
        return bool(self.ordered_list)


def parse_input():
    grid_ = []
    for x, line in enumerate(inp):
        row = []
        for y, sym in enumerate(line.strip()):
            node = Node(sym, x, y)
            row.append(node)
            if sym == 'S':
                start = node
                start.height = 'a'
                start.cost = 1
            elif sym == 'E':
                end = node
                end.height = 'z'
        grid_.append(row)
    return grid_, start, end


def print_grid():
    for row in grid:
        # print(''.join([(f'{n.symbol:2}') for n in row]))
        # print(''.join([f'{n.dist_str():2}' for n in row]))
        print(''.join([f'{n.path_from:1}' for n in row]))


def print_path(from_node, to_node):
    path = set()
    current_node = from_node
    i = 0
    while current_node != to_node:
        path.add(current_node)
        cx, cy = current_node.x, current_node.y
        match current_node.path_from:
            case '>': current_node = grid[cx][cy+1]
            case '<': current_node = grid[cx][cy-1]
            case '^': current_node = grid[cx-1][cy]
            case 'v': current_node = grid[cx+1][cy]
            case _: raise RuntimeError()
    for row in grid:
        print(''.join([f'{n.path_from if n in path else "."}' for n in row]))


def run(grid, start, end, reverse=False):
    queue = Queue()
    queue.insert_or_update(start)
    while queue:
        # print(queue)
        # print_grid()
        current = queue.get_next()
        cx, cy = current.x, current.y
        neighbor_coords = [(cx + 1, cy, '^'), (cx - 1, cy, 'v'), (cx, cy + 1, '<'), (cx, cy - 1, '>')]
        for x, y, direction in neighbor_coords:
            if x < 0 or y < 0:  # really? my solution warped around the edges before.
                continue  # First time i stumbled over unintended negative indexes
            try:
                neighbor = grid[x][y]
                condition = ord(neighbor.height) - 1 <= ord(current.height) if not reverse else ord(current.height) <= ord(neighbor.height) + 1
                if condition:  # reachable
                    new_cost = current.cost + 1
                    if neighbor.cost > new_cost:
                        neighbor.cost = new_cost
                        neighbor.path_from = direction
                        queue.insert_or_update(neighbor)
                    if neighbor in end:
                        return current
            except IndexError:
                continue


grid, start_node, end_node = parse_input()
distance = run(grid, start_node, {end_node}).cost
print_grid()
print()
print_path(end_node, start_node)

print('Distance: ', distance)


grid, _, end_node = parse_input()
end_node.cost = 1
all_a_nodes = [node for row in grid for node in row if node.height == 'a']
closest = run(grid, end_node, all_a_nodes, reverse=True)

print_grid()
print()
print_path(closest, end_node)

print(closest)
print('Distance: ', closest)
