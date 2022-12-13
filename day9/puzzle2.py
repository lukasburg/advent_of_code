import re

with open("input") as file:
    inp = file.readlines()


class Point:
    def __init__(self, x=0, y=0, name=''):
        self.x = x
        self.y = y
        self.name = name

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Unsupported addition between Point and {{{other}}}')
        return Point(self.x + other.x, self.y + other.y)

    def mutable_add(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Unsupported addition between Point and {{{other}}}')
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError(f'Unsupported subtraction between Point and {{{other}}}')
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"{self.name}{self.x, self.y}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)


class MovementVector(Point):
    def __init__(self, p: Point):
        does_move = abs(p.x) > 1 or abs(p.y) > 1
        if does_move:
            x = 1 if p.x > 0 else -1 if p.x < 0 else 0
            y = 1 if p.y > 0 else -1 if p.y < 0 else 0
        else:
            x, y = 0, 0
        super().__init__(x, y)


head = Point(15, 10, 'H')
tails = [Point(15, 10, str(i+1)) for i in range(9)]
leader_follow_pairs = list(zip([head] + tails[:-1], tails))
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
            ('H' if Point(x, y) == head else tails[tails.index(Point(x, y))].name if Point(x, y) in tails else
             '#' if Point(x, y) in touched_points else '.')
            for x in range(size)
        ])
        print(line_str)
    print('---')


for line in inp:
    groups = matcher.search(line).groups()
    direction, number = movements[groups[0]], int(groups[1])
    for i in range(number):
        head.mutable_add(direction)
        for lead, follow in leader_follow_pairs:
            follow.mutable_add(MovementVector(lead - follow))
        touched_points.add(Point(tails[8].x, tails[8].y))
        # print_grid(27)
    # print(movement)

print(len(touched_points))
