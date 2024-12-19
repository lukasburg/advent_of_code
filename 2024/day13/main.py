import re
from itertools import product

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]


def cost(presses: complex):
    return int(3*presses.real + presses.imag)


class Machine:
    def __init__(self, i, ax, ay, bx, by, x, y):
        self.id = i
        self.a_button = complex(ax, ay)
        self.b_button = complex(bx, by)
        self.prize = complex(x, y)
        self.debug = False

    def set_part_two(self):
        self.prize += 10000000000000 + 10000000000000j

    def __str__(self):
        return (f"M{self.id}(A: X+{self.a_button.real}, Y+{self.a_button.imag}, "
                f"B: X+{self.b_button.real},  Y+{self.a_button.real}, "
                f"P(X={self.prize.real}, Y={self.prize.imag}))")

    def solve_for_a(self, b):
        if self.debug:
            print((self.prize - b*self.b_button) / self.a_button)
            # return None
        part_one = (self.prize - b*self.b_button)
        p_real, p_imag = int(part_one.real), int(part_one.imag)
        a_real, a_imag = int(self.a_button.real), int(self.a_button.imag)
        if p_real % a_real == 0 and p_imag % a_imag == 0:
            if p_real // a_real == p_imag // a_imag:
                return p_real // a_real
        return (self.prize - b*self.b_button) / self.a_button

    def solution(self):
        for b in range(101):
            # account for rounding errors
            s = self.solve_for_a(b)
            if isinstance(s, int):
                return complex(s.real, b)
        return None

    def smart_search_solution(self):
        goes_up = self.solve_for_a(0).imag < self.solve_for_a(1).imag
        step = 10000000000000
        current_pos = 0
        previous_pos = current_pos
        while step >= 1:
            current_pos += step
            distance_now = self.solve_for_a(current_pos)
            if isinstance(distance_now, int):
                return complex(distance_now, current_pos)
            distance_now = distance_now.imag
            overstepped = ((not goes_up and distance_now < 0)
                           or (goes_up and distance_now > 0))
            # on overstep
            if overstepped:
                # print(f"Going {'up' if goes_up else 'down'}. "
                #       f"Was on {previous_pos}, went to {current_pos} (+{step}). "
                #       f"Distance is {distance_now}, so 0 was overstepped. "
                #       f"Dividing step by 10.")
                current_pos = previous_pos
                step = step // 10
            else:
                previous_pos = current_pos
        # print("No solution found")
        return None

    def hard_force(self):
        for (x, y) in product(range(101), repeat=2):
            position = x*self.a_button + y*self.b_button
            x_close = self.prize.real - 4 <= position.real <= self.prize.real + 4
            y_close = self.prize.imag - 4 <= position.imag <= self.prize.imag + 4
            if x_close and y_close:
                return x, y
        return None


def parse(string) -> list[Machine]:
    return [Machine(i, *map(int, re.findall("\d+", machine))) for i, machine in enumerate(string.split("\n\n"))]

def run(file="input.txt"):
    machines = parse(read(file))
    print(sum([cost(s) for m in machines if (s := m.solution())]))
    for m in machines:
        m.set_part_two()
    print(sum([cost(s) for m in machines if (s := m.smart_search_solution())]))
    # solution = m.smart_search_solution()
    # if solution:
    #     print(f'found solution: {solution}')
    #     print(f'Cost {cost(solution)}')
    # print('\n')

if __name__ == "__main__":
    run("example.txt")
    run()
