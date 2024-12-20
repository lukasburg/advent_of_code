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
    return towels, designs

def create_matcher(towels):
    return re.compile(
        "(" + "|".join([f"({towel.strip()})" for towel in towels]) + ")*"
    )

def is_valid_design(design, matcher):
    if matcher.fullmatch(design):
        return True
    return False

def run(file="input.txt"):
    towels, designs = parse(read(file))
    matcher = create_matcher(towels)
    t = [is_valid_design(design, matcher) for design in designs]
    return t.count(True)

if __name__ == "__main__":
    print(run("example.txt"))
    print(run())
