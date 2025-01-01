class Map:
    directions = [1+0j, 0+1j, -1+0j, 0-1j]
    directions_symbols = {1+0j: '>', 0+1j: 'v', -1+0j: '<', 0-1j: '^',
                          '>': 1+0j, 'v': 0+1j, '<': -1+0j, '^': 0-1j}

    def __init__(self, array_map):
        self.array_map = array_map
        self.x_max = len(array_map[0])
        self.y_max = len(array_map)

    def __getitem__(self, k: complex | tuple):
        if isinstance(k, complex):
            return self.array_map[int(k.imag)][int(k.real)]
        return self.array_map[k[1]][k[0]]

    def __setitem__(self, k: complex | tuple, value):
        if isinstance(k, complex):
            self.array_map[int(k.imag)][int(k.real)] = value
        else:
            self.array_map[k[1]][k[0]] = value

    def neighbors(self, k: complex | tuple):
        if isinstance(k, complex):
            return {k + d for d in self.directions}
        else:
            return {(k[0] + int(d.real), k[1] + int(d.imag)) for d in self.directions}

    def is_inbounds(self, k: complex | tuple):
        if isinstance(k, complex):
            return 0 <= int(k.imag) < self.y_max and 0 <= int(k.real) < self.x_max
        return 0 <= k[1] < self.y_max and 0 <= k[0] < self.x_max

    def coords_in_radius_of(self, k: complex | tuple, radius: int):
        in_radius = set()
        if isinstance(k, complex):
            x, y = int(k.real), int(k.imag)
        else:
            x, y = k[0], k[1]
        for d in range(radius+1):
            for x_part in range(d+1):
                y_part = d - x_part
                all_four_directions = {(x_part, y_part), (-x_part, y_part), (x_part, -y_part), (-x_part, -y_part)}
                real_coords = {(x + x_d, y + y_d) for x_d, y_d in all_four_directions}
                real_coords_inbounds = filter(self.is_inbounds, real_coords)
                if isinstance(k, complex):
                    real_coords_inbounds = map(lambda d: complex(d[0], d[1]), real_coords_inbounds)
                in_radius.update(real_coords_inbounds)
        return in_radius

    def __iter__(self):
        return iter(self.array_map)

    def __str__(self):
        return '\n'.join([''.join([str(self[x, y]) for x in range(self.x_max)]) for y in range(self.y_max)])

    @classmethod
    def from_string(cls, string) -> 'Map':
        m = [[s for s in line] for line in string.split('\n')]
        return cls(m)

    @classmethod
    def empty_map(cls, size):
        if isinstance(size, complex):
            size = int(size.real), int(size.imag)
        if isinstance(size, tuple):
            return cls([['.' for _ in range(size[0])] for _ in range(size[1])])
        return cls([['.' for _ in range(size)] for _ in range(size)])

    def find_symbol(self, symbol):
        for y, line in enumerate(self.array_map):
            for x, sym in enumerate(line):
                if sym == symbol:
                    return complex(x, y)
        raise ValueError('Symbol not found')

    def find_all_symbols(self, symbol):
        coord_set = set()
        for y, line in enumerate(self.array_map):
            for x, sym in enumerate(line):
                if sym == symbol:
                    coord_set.add(complex(x, y))
        return coord_set

    def breath_first_search_width_paths(self, start_pos, end_pos, wall_symbol='#'):
        paths = [(start_pos,)]
        while paths:
            current_path = paths.pop(0)
            current_pos = current_path[-1]
            for n in self.neighbors(current_pos):
                if not self.is_inbounds(n) or n in current_path:
                    continue
                if n == end_pos:
                    return current_path + (n,)
                if not wall_symbol is None and self[n] != wall_symbol:
                    paths.append(current_path + (n,))
        raise ValueError('No path found')

    def distance_search(self, start_pos, end_pos, wall_symbol='#'):
        def is_wall(c):
            if wall_symbol is None:
                return False
            return self[c] == wall_symbol

        outer_perimeter = {start_pos}
        visited = set()
        d = 0
        while outer_perimeter:
            if end_pos in outer_perimeter:
                return d
            d += 1
            new_outer_perimeter = set()
            for cell in outer_perimeter:
                for neighbor in self.neighbors(cell):
                    if self.is_inbounds(neighbor) and not is_wall(neighbor) and neighbor not in visited:
                        new_outer_perimeter.add(neighbor)
            visited.update(outer_perimeter)
            outer_perimeter = new_outer_perimeter
        raise ValueError('No path found')

def distance(k1: complex | tuple, k2: complex | tuple):
    if isinstance(k1, tuple):
        k1 = complex(*k1)
        k2 = complex(*k2)
    d = k1 - k2
    d = abs(int(d.real)) + abs(int(d.imag))
    return d

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]
