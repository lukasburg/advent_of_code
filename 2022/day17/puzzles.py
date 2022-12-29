class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'P(x={self.x}, y={self.y})'

    def __repr__(self):
        return str(self)


class Rock:
    def __init__(self, start_pos: Point, points):
        self.positions = set()
        self.main_pos = start_pos
        self.points = points

