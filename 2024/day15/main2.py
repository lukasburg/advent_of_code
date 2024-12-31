import helpers

WALL = '#'

def double_x(k):
    return complex(k.real*2, k.imag)

class WallError(Exception):
    pass

class Box:
    def __init__(self, pos, on_map):
        self.pos = (pos, pos+1)
        self.on_map = on_map

    def __str__(self):
        return '['

    def move(self, direction):
        boxes = self._find_move_set(direction)
        for box in boxes:
            box._move_self(direction)

    def _find_move_set(self, direction):
        if self.on_map[self.pos[0] + direction] == WALL or self.on_map[self.pos[1] + direction] == WALL:
            raise WallError
        move_set = {self}
        left = self.on_map[self.pos[0] + direction]
        if isinstance(left, Box) and direction in {-1j, 1j, -1}:
            # recursive find left side
            move_set.update(left._find_move_set(direction))
        right = self.on_map[self.pos[1] + direction]
        if isinstance(right, Box) and direction in {-1j, 1j, 1}:
            # recursive find right side
            move_set.update(right._find_move_set(direction))
        return move_set

    def _move_self(self, direction):
        if self.on_map[self.pos[0]] == self:
            self.on_map[self.pos[0]] = '.'
        if self.on_map[self.pos[1]] == self:
            self.on_map[self.pos[1]] = '.'
        self.pos = (self.pos[0] + direction, self.pos[1] + direction)
        self.on_map[self.pos[0]] = self
        self.on_map[self.pos[1]] = self

    def gps_score(self):
        x, y = int(self.pos[0].real), int(self.pos[0].imag)
        return 100*y + x

class Robot:
    def __init__(self, start_pos, on_map):
        self.on_map = on_map
        self.pos = start_pos

    def move(self, direction):
        next_field = self.on_map[self.pos + direction]
        if next_field == WALL:
            raise WallError
        if isinstance(next_field, Box):
            next_field.move(direction)
        self.on_map[self.pos] = '.'
        self.pos = self.pos + direction
        self.on_map[self.pos] = self

    def __str__(self):
        return '@'

def alphabet_generator():
    for i in range(65, 89):
        yield chr(i)

def create_double_warehouse(map_string):
    half_warehouse = helpers.Map.from_string(map_string)
    walls_set = half_warehouse.find_all_symbols(WALL)
    boxes_set = half_warehouse.find_all_symbols('O')
    warehouse = helpers.Map([['.' for _ in range(half_warehouse.x_max*2)] for _ in range(half_warehouse.y_max)])
    start_pos = double_x(half_warehouse.find_symbol('@'))
    warehouse[start_pos] = '@'
    # print(doubled_map)
    alph = alphabet_generator()
    for wall in walls_set:
        warehouse[double_x(wall)] = WALL
        warehouse[double_x(wall) + 1] = WALL
    boxes = set()
    for box_pos in boxes_set:
        box = Box(double_x(box_pos), warehouse)
        warehouse[box.pos[0]] = box
        warehouse[box.pos[1]] = box
        boxes.add(box)
    return warehouse, boxes

def parse_instructions(instructions):
    return [helpers.Map.directions_symbols[i] for i in instructions if i != '\n']

def run(filename='input.txt'):
    map_string, instructions = helpers.read(filename).split('\n\n')
    warehouse, boxes = create_double_warehouse(map_string)
    instructions = parse_instructions(instructions)
    robot = Robot(warehouse.find_symbol('@'), warehouse)
    for instruction in instructions:
        # print(warehouse)
        try:
            # print(helpers.Map.directions_symbols[instruction])
            robot.move(instruction)
        except WallError:
            pass
            # print(f'Ignored {helpers.Map.directions_symbols[instruction]}')
    print(sum([box.gps_score() for box in boxes]))

if __name__ == '__main__':
    run('example.txt')
    run()
