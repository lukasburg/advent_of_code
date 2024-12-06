from pprint import pprint

with open("input") as file:
    inp = file.read()


direction = complex
dir_to_str = {
    1: '>',
    -1: '<',
    1j: 'v',
    -1j: '^'
}


class Beam:
    def __init__(self, position: complex, beam_dir: direction):
        self.direction = beam_dir
        self.position = position

    def __str__(self):
        return f"{self.position}(±{self.direction})"


class Field:
    def __init__(self, symbol):
        self.symbol = symbol
        self.has_beam_direction: set[direction] = set()

    def manipulate_beam(self, beam_direction: direction) -> set[direction]:
        if self.symbol == '.':
            return self._empty_manipulate_beam(beam_direction)
        elif self.symbol == '-' or self.symbol == '|':
            return self._splitter_manipulate_beam(beam_direction)
        elif self.symbol == '/' or self.symbol == '\\':
            return self._mirror_manipulate_beam(beam_direction)
        else:
            raise NotImplemented

    def _empty_manipulate_beam(self, beam_direction: direction):
        return {beam_direction}

    def _mirror_manipulate_beam(self, beam_direction: direction):
        clockwise = True
        if self.symbol == '\\' and beam_direction.imag == 0:
            clockwise = False
        elif self.symbol == '/' and beam_direction.real == 0:
            clockwise = False
        if clockwise:
            return {beam_direction*-1j}
        else:
            return {beam_direction*1j}

    def _splitter_manipulate_beam(self, beam_direction: direction):
        if self.symbol == '-':
            if beam_direction.imag == 0:
                return {beam_direction}
            else:
                return {1, -1}
        elif self.symbol == '|':
            if beam_direction.real == 0:
                return {beam_direction}
            else:
                return {1j, -1j}

    def render(self):
        if self.symbol == '.':
            if len(self.has_beam_direction) > 1:
                return str(len(self.has_beam_direction))
            elif len(self.has_beam_direction) == 1:
                direction = self.has_beam_direction.pop()
                self.has_beam_direction.add(direction)
                return dir_to_str[direction]
        return self.symbol

    def is_energized(self):
        return len(self.has_beam_direction) >= 1


def parse(str_inp):
    parsed_map = []
    for line in str_inp[:-1].split('\n'):
        parsed_map.append([Field(symbol) for symbol in line])
    return parsed_map


class Map:
    def __init__(self, str_inp: str):
        self.map = parse(str_inp)

    def __getitem__(self, item):
        return self.map[int(item.imag)][int(item.real)]

    @property
    def size(self):
        return len(self.map[0]), len(self.map)

    def render(self):
        lines = []
        for line in self.map:
            lines.append(''.join([field.render() for field in line]))
        return '\n'.join(lines)

    def beam_inside_map(self, beam: Beam):
        return 0 <= beam.position.imag < len(self.map) and 0 <= beam.position.real < len(self.map[0])

    def count_energized(self):
        return len(list(filter(lambda f: f.is_energized(), [field for line in self.map for field in line])))


def energy_on_map(start_pos, start_dir, mirror_map):
    # print(mirror_map.render())
    start_beam = Beam(start_pos, start_dir)
    current_beams = {start_beam}
    # render_once = False
    while current_beams:
        new_current_beams = set()
        for beam in current_beams:
            on_field = mirror_map[beam.position]
            move_directions = on_field.manipulate_beam(beam.direction)
            for move_dir in move_directions:
                if move_dir in on_field.has_beam_direction:
                    continue
                else:
                    on_field.has_beam_direction.add(move_dir)
                    new_beam = Beam(beam.position + move_dir, move_dir)
                    if mirror_map.beam_inside_map(new_beam):
                        new_current_beams.add(new_beam)
        current_beams = new_current_beams
        # if render_once:
        #     print(mirror_map.render())
        #     render_once = False
        #     print('\n\n---\n')
        # print(mirror_map.render())
    return mirror_map.count_energized()


def run():
    mirror_map = Map(inp)
    # print(f"Energized: {energy_on_map(0, 1, Map(inp))}")

    width, height = mirror_map.size
    starts = ([(i, 1j) for i in range(width)] + [(complex(0, i), 1) for i in range(height)] +
              [(complex(i, height-1), -1j) for i in range(width)] + [(complex(width-1, i), -1) for i in range(height)])
    max_energy = max(energy_on_map(*start, Map(inp)) for start in starts)
    print(f'Max energy {max_energy}')


if __name__ == "__main__":
    run()
