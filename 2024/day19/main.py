import re

class Memory:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"(A:{self.a} B:{self.b} C:{self.c})"

def read(filename="input.txt"):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    towels_string, designs_string = string.split("\n\n")
    towels = towels_string.split(",")
    designs = designs_string.split("\n")
    return [towel.strip() for towel in towels], designs

def create_matcher(towels):
    return re.compile(
        "(" + "|".join([f"({towel})" for towel in towels]) + ")*"
    )

def is_valid_design(design, matcher):
    if matcher.fullmatch(design):
        return True
    return False

cache = dict()

def recursive_match(towels: list[str], design: str, matcher):
    if design == '':
        # print(f"Finished subtree after {depth}")
        return 1
    if design in cache:
        return cache[design]
    sub_designs = []
    for towel in towels:
        if design.startswith(towel) and is_valid_design(design[len(towel):], matcher):
            sub_designs.append(design[len(towel):])
    total_sum = 0
    for i, sub_design in enumerate(sub_designs):
        total_sum += recursive_match(towels, sub_design, matcher)
    cache[design] = total_sum
    return total_sum


def run(file="input.txt"):
    towels, designs = parse(read(file))
    matcher = create_matcher(towels)
    valid = [is_valid_design(design, matcher) for design in designs]
    variations = sum([recursive_match(towels, design, matcher) for design in designs])
    return valid.count(True), variations

if __name__ == "__main__":
    # print(run("example.txt"))
    print(run())
