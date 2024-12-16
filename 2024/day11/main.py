def read(filename):
    with open(filename) as file:
        string = file.read()[:-1]
        return string

def parse(string):
    stone_numbers = [int(number) for number in string.split(" ")]
    next_stone = None
    for number in reversed(stone_numbers):
        next_stone = Stone(number, next_stone)
    return next_stone

class Stone:
    def __init__(self, start_value: int, next_stone = None):
        self.value = start_value
        self.next_stone = next_stone

    def split(self):
        as_string = str(self.value)
        first_digits = as_string[:len(as_string) // 2]
        last_digits = as_string[len(as_string)//2:]
        self.value = int(first_digits)
        self.next_stone = Stone(int(last_digits), self.next_stone)

    def blink(self):
        if self.value == 0:
            self.value = 1
        elif len(str(self.value)) % 2 == 0:
            self.split()
        else:
            self.value *= 2024

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class StoneIterator:
    def __init__(self, start_stone: Stone):
        self.current_stone = start_stone
        self.starting = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.starting:
            self.starting = False
            return self.current_stone
        else:
            self.current_stone = self.current_stone.next_stone
            if self.current_stone is None:
                raise StopIteration
            return self.current_stone

def run(file='input.txt', blinks=25):
    start_stone = parse(read(file))
    for i in range(blinks):
        # print(", ".join([str(stone) for stone in StoneIterator(start_stone)]))
        # print(i, len(list(StoneIterator(start_stone))))
        print(i, len(list(StoneIterator(start_stone))), list(StoneIterator(start_stone)))
        for stone in list(StoneIterator(start_stone)):
            stone.blink()
    return len(list(StoneIterator(start_stone)))



if __name__ == "__main__":
    print(run("example.txt"))
    # print(run())
