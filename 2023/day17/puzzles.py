from typing import Optional

# Funktioniert nicht:
# Pfade werden gekürzt, sobald ein kürzerer bekannt ist.
# Wegen der Regel, dass Pfade nicht drei mal in die gleiche Richtung fahren dürfen, ist es aber möglich
# das ein Pfad, der schlechter abgeschnitten hat bis zum punkt x, danach den anderen pfad noch überholt, weil er
# noch länger in eine bestimmte richtung darf

with open("example_input") as file:
    inp = file.read()

dir_to_str = {
    0: 'S',
    1: '>',
    -1: '<',
    1j: 'v',
    -1j: '^'
}


class Field:
    def __init__(self, coordinate, heat_loss, is_finish=False):
        self.heat_loss = heat_loss
        self.symbol = str(heat_loss)
        self.is_finish = is_finish
        self.best_paths: dict[str, list[tuple[int, Optional['Path']]]] = {
            c: [(99999, None), (99999, None), (99999, None)] for c in dir_to_str.keys()
        }
        self.coordinate = coordinate

    def update_best_paths(self, path: 'Path'):
        for heat_loss, known_path in self.best_paths[path.direction][:path.number_of_moves_in_same_dir]:
            if heat_loss <= path.total_heat_loss:
                return False
        for index, t in enumerate(self.best_paths[path.direction][path.number_of_moves_in_same_dir-1:]):
            heat_loss, known_path = t
            if heat_loss >= path.total_heat_loss:
                if known_path:
                    known_path.stop_self_and_paths_from_here()
                # is path here okay, although it is maybe too high?
                self.best_paths[path.direction][index] = (path.total_heat_loss, path)
        return True

    def best_path(self):
        minimum = 99999
        best_path = None
        for dir_list in self.best_paths.values():
            for heat_loss, path in dir_list:
                if heat_loss < minimum:
                    minimum = heat_loss
                    best_path = path
        return best_path

    def __str__(self):
        return f"(+{self.heat_loss}) "


def parse(str_inp) -> list[list[Field]]:
    parsed_map = []
    for y, line in enumerate(str_inp[:-1].split('\n')):
        parsed_map.append([Field(complex(x, y), int(heat_loss)) for x, heat_loss in enumerate(line)])
    return parsed_map


class Map:
    def __init__(self, str_inp: str):
        self.finish: Field = None
        self.map = parse(str_inp)
        self.set_finish()

    def __getitem__(self, item) -> Field:
        if item.imag < 0 or item.real < 0:
            raise IndexError
        return self.map[int(item.imag)][int(item.real)]

    def set_finish(self):
        self.finish = self.map[len(self.map) - 1][len(self.map[0]) - 1]
        self.finish.is_finish = True

    @property
    def size(self):
        return len(self.map[0]), len(self.map)

    def render(self):
        lines = []
        for line in self.map:
            lines.append(''.join([str(field) for field in line]))
        return '\n'.join(lines)

    def render_final_path(self):
        self.finish.best_path().render_path()
        lines = []
        for line in self.map:
            lines.append(''.join([field.symbol for field in line]))
        return '\n'.join(lines)


class Path:
    directions = dir_to_str.keys()

    def __init__(self, heat_map: Map, next_step_direction, parent_path: 'Path' = None, number_of_moves_in_same_dir=1):
        self.parent_path = parent_path
        self.paths_from_here: set['Path'] = set()
        self.heat_map = heat_map
        self.direction = next_step_direction
        self.number_of_moves_in_same_dir = number_of_moves_in_same_dir
        if parent_path:
            self.on_field = heat_map[parent_path.on_field.coordinate + next_step_direction]
            self.total_heat_loss = parent_path.total_heat_loss + self.on_field.heat_loss
        else:
            self.on_field = heat_map[next_step_direction]
            self.total_heat_loss = self.on_field.heat_loss
        self.continue_path = self.on_field.update_best_paths(self)

    def is_on_finish(self):
        return self.on_field.is_finish

    def generate_next_subpaths(self) -> set["Path"]:
        subpaths = set()
        if self.continue_path and not self.is_on_finish():
            for next_dir in self.directions:
                number_of_same_moves_next = self.number_of_moves_in_same_dir + 1 if self.direction == next_dir else 1
                if number_of_same_moves_next <= 3 and next_dir != -self.direction:
                    try:
                        path = Path(self.heat_map, next_dir, self, number_of_same_moves_next)
                        subpaths.add(path)
                    except IndexError:
                        pass
        return subpaths

    def stop_self_and_paths_from_here(self):
        self.continue_path = True
        for path in self.paths_from_here:
            path.stop_self_and_paths_from_here()

    def __str__(self):
        x, y = self.on_field.coordinate.real, self.on_field.coordinate.imag
        return f"Path(x={x}, y={y}, heat_loss={self.total_heat_loss}, nr_same_dir={self.number_of_moves_in_same_dir})"

    def render_path(self):
        self.on_field.symbol = dir_to_str[self.direction]
        if self.parent_path:
            self.parent_path.render_path()


def run(input_string):
    heat_map = Map(input_string)
    first_path = Path(heat_map, 0)
    current_paths = {first_path}
    while current_paths:
        next_paths = set()
        for path in current_paths:
            next_paths = next_paths.union(path.generate_next_subpaths())
        current_paths = next_paths
        # print(heat_map.render())
        # print('\n\n\n')
    print(min([item[0] for tuple_list in heat_map.finish.best_paths.values() for item in tuple_list]))
    print(heat_map.render_final_path())


if __name__ == "__main__":
    run(inp)
