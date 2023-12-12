with open("example_input") as file:
    inp = file.readlines()

parser = {
    "J": ("\u255D", {complex(-1), -1j}),
    "L": ("\u255A", {complex(1), -1j}),
    "F": ("\u2554", {complex(1), 1j}),
    "7": ("\u2557", {complex(-1), 1j}),
    "-": ("\u2550", {complex(-1), complex(1)}),
    "|": ("\u2551", {-1j, 1j}),
    ".": (" ", set()),
    "S": ("S", set())
}


class Pipe:
    def __init__(self, str_in_input, pos_x, pos_y, is_padding=False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        str_repr, direction = parser[str_in_input]
        self.symbol = str_repr
        self.dirs = direction
        self.in_loop = False
        self.outside_loop = None
        self.is_padding = is_padding

    def render(self):
        if self.outside_loop:
            return 'o'
        if not self.in_loop:
            return '.'
        return self.symbol

    def __str__(self):
        return f"Pipe(x: {self.pos_x}, y: {self.pos_y}, {self.symbol})"

    def __repr__(self):
        return str(self)

    def next_pipe_direction(self, coming_from):
        self.in_loop = True
        return self.dirs.difference(coming_from).pop()


def render_map(t_map):
    for row in t_map:
        print(''.join(map(lambda r: r.render(), row)))


total_map = []
for y, line in enumerate(inp):
    row = []
    for x, symbol in enumerate(line[:-1]):
        pipe = Pipe(symbol, x, y)
        row.append(pipe)
        if symbol == "S":
            start = pipe
            start.in_loop = True
    total_map.append(row)


# find two start positions
connected_to_start: list[Pipe] = []
comming_from: list[complex] = []
sx = start.pos_x
sy = start.pos_y
if complex(-1) in total_map[sy][sx+1].dirs:
    connected_to_start.append(total_map[sy][sx+1])
    comming_from.append(complex(1))
if complex(1) in total_map[sy][sx-1].dirs:
    connected_to_start.append(total_map[sy][sx-1])
    comming_from.append(complex(-1))
if -1j in total_map[sy+1][sx].dirs:
    connected_to_start.append(total_map[sy+1][sx])
    comming_from.append(1j)
if 1j in total_map[sy-1][sx].dirs:
    connected_to_start.append(total_map[sy-1][sx])
    comming_from.append(-1j)

s1 = connected_to_start[0]
s2 = connected_to_start[1]
c1, c2 = comming_from
i = 0
while s1 != s2:
    c1 = s1.next_pipe_direction({-c1})
    s1 = total_map[s1.pos_y+int(c1.imag)][s1.pos_x+int(c1.real)]
    c2 = s2.next_pipe_direction({-c2})
    s2 = total_map[s2.pos_y+int(c2.imag)][s2.pos_x+int(c2.real)]
    i += 1
s1.in_loop = True

render_map(total_map)
print(f"Farthest reached after {i+1} steps")
print("\n---\n")


def expand_map(t_map):
    padded_map = []
    for y, row in enumerate(t_map):
        padded_row = []
        empty_row = [Pipe(".", x, y*2+1, is_padding=True) for x in range(len(row)*2)]
        for place in row:
            place.pos_y = place.pos_y*2
            place.pos_x = place.pos_x*2
            padded_row.append(place)
            padded_row.append(Pipe(".", place.pos_x+1, place.pos_y, is_padding=True))
        padded_map.append(padded_row)
        padded_map.append(empty_row)
    for pipe in filter(lambda p: p.in_loop, [pipe for row in padded_map for pipe in row]):
        for direction in pipe.dirs:
            neighbor = padded_map[pipe.pos_y+int(direction.imag)][pipe.pos_x+int(direction.real)]
            neighbor.in_loop = True
            neighbor.symbol = "x"
    return padded_map


def flood_fill(t_map):
    top = t_map[0]
    bottom = t_map[-1]
    left = [row[0] for row in t_map]
    right = [row[-1] for row in t_map]
    outer: set[Pipe] = set(filter(lambda p: not p.in_loop, top+bottom+left+right))
    while outer:
        new_outer = set()
        for place in outer:
            place.outside_loop = True
            neighbors = [
                t_map[place.pos_y-1][place.pos_x],
                t_map[(place.pos_y+1) % len(t_map)][place.pos_x],
                t_map[place.pos_y][place.pos_x-1],
                t_map[place.pos_y][(place.pos_x+1) % len(t_map[0])],
            ]
            for floodable_neighbor in filter(lambda p: not p.in_loop and not p.outside_loop, neighbors):
                new_outer.add(floodable_neighbor)
        outer = new_outer
    print("Flood map:")
    render_map(t_map)
    return len(list(filter(lambda p: not p.in_loop and not p.outside_loop and not p.is_padding, [place for row in total_map for place in row])))


padded_map = expand_map(total_map)
print("Pad map with empty nodes, to fill through gaps:")
render_map(padded_map)
print("\n---\n")
print(f"Places inside loop: {flood_fill(padded_map)}")
