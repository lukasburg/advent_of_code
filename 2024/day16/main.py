from itertools import starmap
from functools import reduce
from operator import neg
import numpy as np


WALL = '\u2588'


d_to_sym = {
    (1, 0): 'v',
    (-1, 0): '^',
    (0, 1): '>',
    (0, -1): '<',
}

def read(filename="input.txt"):
    with open(filename) as file:
        return file.read()[:-1]


def parse(string):
    lines = string.split('\n')
    a = np.full((len(lines[0]), len(lines)), ' ', dtype=np.dtype('U1'))
    start = -1, -1
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == '#':
                a[x, y] = WALL
            elif char == 'E':
                a[x, y] = 'E'
            elif char == 'S':
                start = complex(x, y)
    return a, start


def step_score(dir1, dir2):
    return 1 if dir1 == dir2 else 1001
    
def path_score(path, start_dir=(1, 0)):
    return sum(starmap(step_score, zip(
            [start_dir] + path[:-1], path
        )))

def n(d):
    return tuple(map(neg, d))
    
def position(path, start_pos):
    c = sum([start_pos] + path)
    return int(c.real), int(c.imag)

def next_dirs():
    return {
        1+0j, -1+0j, 0+1j, 0-1j
    }

def next_paths(path, maze):
    new_paths = []
    for next_dir in next_dirs():
        next_path = path.move(next_dir)
        try:
            if not next_path.pos in path.visited and maze[next_path.coord()] != WALL:
                # skip if visited or is wall
                new_paths.append(next_path)
        except IndexError:
            # is out of bounds, skip
            continue
    return new_paths

def render_maze(maze):
    return '\n'.join([''.join(line for line in maze[y]) for y in range(len(maze))])

class Path:
    def __init__(self, pos, last_direction, visited, score):
        self.pos = pos
        self.last_direction = last_direction
        self.visited = visited
        self.score = score

    def coord(self):
        return int(self.pos.real), int(self.pos.imag)

    def move(self, next_direction):
        score = self.score + 1
        if self.last_direction != next_direction:
            score += 1000
        new_pos = self.pos + next_direction
        visited = self.visited.union({new_pos})
        return Path(new_pos, next_direction, visited, score)


def depth_first_search(maze, start_pos):
    paths = [Path(start_pos, 1+0j, set(), 0)]
    min_score = 999999999999999999999999
    i = 0
    while paths:
        i += 1
        current = paths.pop()
        if i % 100000 == 0:
            print(render_maze(maze))
            print("--------")
        if maze[current.coord()] == "E":
            # reached fin
            if current.score < min_score:
                min_score = current.score
                min_path = current
                print(f"New lowest score: {min_score}, path: {current}")
            continue
        else:
            if current.score > min_score:
                # do not continue if already higher than lowest minimum
                maze[current.coord()] = '\u16ED'
                continue
            else:
                next_options = next_paths(current, maze)
                if len(next_options) == 0:
                    maze[current.coord()] = 'x'
                if len(next_options) == 1:
                    maze[current.coord()] = '.'
                if len(next_options) > 1:
                    maze[current.coord()] = 'O'
                paths += next_options
    return min_score

def run(file="input.txt"):
    maze, start_pos = parse(read(file))
    print(depth_first_search(maze, start_pos))

    
if __name__ == "__main__":
    run("example.txt")
    run("example2.txt")
    run()
