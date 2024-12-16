import main
from collections import defaultdict

def read(filename):
    with open(filename) as file:
        string = file.read()[:-1]
        return string

def parse(string):
    return [int(number) for number in string.split(" ")]
    # return stone_numbers

known_values = dict()
heap = defaultdict(list)

def split(value):
    as_string = str(value)
    first_digits = as_string[:len(as_string) // 2]
    last_digits = as_string[len(as_string) // 2:]
    return int(first_digits), int(last_digits)

def blink(value):
    if value == 0:
        return (1, )
    elif len(str(value)) % 2 == 0:
        return split(value)
    else:
        return (value*2024, )

class Lazy:
    def __init__(self, remaining_blinks, stones):
        self.stones = stones
        self.remaining_blinks = remaining_blinks

    def __repr__(self):
        return f"L({self.remaining_blinks}: {self.stones})"

    def solve(self, remaining_blinks=None):
        rb = remaining_blinks if (remaining_blinks is not None) else self.remaining_blinks
        heap[rb].append(self.stones)
        total_sum = 0
        if rb <= 0:
            return len(self.stones)
        for stone in self.stones:
            if stone not in known_values:
                total_sum += 1
            else:
                res = known_values[stone].solve(rb-1)
                total_sum += res
        return total_sum

def go_through(stone, remaining_blinks=6):
    if remaining_blinks <= 0:
        return
    next_stones = blink(stone)
    known_values[stone] = Lazy(remaining_blinks-1, next_stones)
    for stone in next_stones:
        if stone not in known_values:
            go_through(stone, remaining_blinks-1)

def run(blinks, file='input.txt'):
    stones = parse(read(file))
    for stone in stones:
        go_through(stone, blinks)
    total_stones = 0
    for stone in stones:
        total_stones += known_values[stone].solve()
    print(0, stones)
    for i in reversed(range(blinks)):
        unwrapped_list = [b for a in heap[i] for b in a]
        print(blinks - i, len(unwrapped_list), unwrapped_list) # (unwrapped_list))
    return total_stones

if __name__ == "__main__":
    print(run(9, "example.txt"))
    print('\n')
    main.run("example.txt", 9+1)
