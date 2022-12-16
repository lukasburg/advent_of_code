import re

with open("input") as file:
    inp = file.readlines()


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Unsupported addition between Point and {{{other}}}')
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Unsupported subtraction between Point and {{{other}}}')
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"P{self.x, self.y}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)


class MovementVector(Point):
    def __init__(self, p: Point):
        x = p.x if abs(p.y) > 1 else p.x - 1 if p.x > 0 else p.x+1 if p.x < 0 else 0
        y = p.y if abs(p.x) > 1 else p.y - 1 if p.y > 0 else p.y+1 if p.y < 0 else 0
        super().__init__(x, y)


head = Point(0, 0)
tail = Point(0, 0)
touched_points = set()

matcher = re.compile("(.) (\d+)")
movements = {
    'U': Point(0, 1),
    'R': Point(1, 0),
    'D': Point(0, -1),
    'L': Point(-1, 0)
}


def print_grid(size=6):
    for y in range(size)[::-1]:
        line_str = ' '.join([
            ('H' if Point(x, y) == head else 'T' if Point(x, y) == tail else
             '#' if Point(x, y) in touched_points else '.')
            for x in range(size)
        ])
        print(line_str)


for line in inp:
    groups = matcher.search(line).groups()
    direction, number = movements[groups[0]], int(groups[1])
    for i in range(number):
        head += direction
        tail += MovementVector(head - tail)
        touched_points.add(tail)
        # print(head, tail)
        # print_grid()
    # print(movement)

print(len(touched_points))
