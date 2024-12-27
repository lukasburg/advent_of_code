from collections import defaultdict
from functools import reduce
from itertools import starmap
import numpy as np
from queue import PriorityQueue
import progressbar as pb

WALL = '#'
d_to_sym = {
    1 + 0j: 'v',
    -1 + 0j: '^',
    0 + 1j: '>',
    0 +-1j: '<',
}

def read(filename="input.txt"):
    with open(filename) as file:
        return file.read()[:-1]


def parse(string):
    lines = string.split('\n')
    a = np.full((len(lines[0]), len(lines)), ' ')
    start = -1, -1
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == '#':
                a[x, y] = "#"
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

def next_dirs():
    return {
        1+0j, -1+0j, 0+1j, 0-1j
    }

def update_maze_lowest_possible_score(pos, direction, score, lowest_scores):
    if lowest_scores[(pos, direction)] == -1:
        lowest_scores[(pos, direction)] = score
        return True
    if score <= lowest_scores[(pos, direction)]:
        lowest_scores[(pos, direction)] = score
        return True
    return False

def next_paths(path, maze, lowest_scores):
    new_paths = []
    for next_dir in next_dirs():
        next_path = path.move(next_dir)
        try:
            if not next_path.pos in path.visited and maze[next_path.coord()] != WALL:
                # skip if visited or is wall
                if update_maze_lowest_possible_score(path.coord(), next_dir, next_path.score, lowest_scores):
                    # skip if better path to pos is known
                    new_paths.append(next_path)
                # else:
                #     print(f'Path {next_path} was skipped:')
                #     render_maze(maze, next_path)
        except IndexError:
            # is out of bounds, skip
            continue
    return new_paths

def render_maze(maze, path: 'Path'):
    sym = maze[path.coord()]
    maze[path.coord()] = 'O'
    prev = complex(*path.coord()) - path.last_direction
    maze[int(prev.real), int(prev.imag)] = d_to_sym[path.last_direction]
    print('\n'.join([''.join([maze[y, x] for x in range(len(maze[0]))]) for y in range(len(maze))]))
    maze[path.coord()] = sym
    maze[int(prev.real), int(prev.imag)] = ' '

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

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score

    def __str__(self):
        return f"P({self.pos}, {self.last_direction}, {self.score})"

    def __repr__(self):
        return str(self)

def breadth_first_search(maze, start_pos):
    queue: PriorityQueue[Path] = PriorityQueue()
    queue.put(Path(start_pos, 0 + 1j, set(), 0))
    lowest_scores = defaultdict(lambda: -1)
    solutions = []
    with pb.ProgressBar(max_value=pb.UnknownLength, widgets=[
        ' [', pb.Timer(), '] ',
        pb.Bar(),
        pb.widgets.Variable('score')
    ]) as p:
        while not queue.empty():
            current = queue.get()
            # render_maze(maze, current)
            p.update(score=current.score)
            for next_path in next_paths(current, maze, lowest_scores):
                queue.put(next_path)
                if maze[next_path.coord()] == 'E':
                    solutions.append(next_path)
    print(solutions)
    return sorted(solutions, key=lambda c: c.score)



def run(file="input.txt"):
    maze, start_pos = parse(read(file))
    solution_paths = breadth_first_search(maze, start_pos)
    lowest_score = solution_paths[0].score
    all_visited = set(reduce(set.union, map(lambda p: p.visited, filter(lambda p: p.score == lowest_score, solution_paths))))
    return lowest_score, len(all_visited) + 1

    
if __name__ == "__main__":
    print(run("example.txt"))
    print(run("example2.txt"))
    print(run())
