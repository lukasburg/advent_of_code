class Symbol:
    value = None

    @staticmethod
    def create(string) -> 'Symbol':
        if string in ('A', 'X'):
            return Rock()
        elif string in ('B', 'Y'):
            return Paper()
        elif string in ('C', 'Z'):
            return Scissor()

    def create_response(self, string) -> 'Symbol':
        if string == 'X':       # lose
            return self.beats
        elif string == 'Y':     # draw
            return self.__class__()
        elif string == 'Z':     # win
            return self.looses

    @property
    def beats(self): raise NotImplemented
    @property
    def looses(self): raise NotImplemented

    def __eq__(self, other):
        return isinstance(other, type(self))

    def against(self, other):
        if other == self:
            return 3
        elif self.beats == other:
            return 6
        elif self.looses == other:
            return 0

    def __str__(self):
        return self.__class__.__name__


class Rock(Symbol):
    value = 1

    @property
    def beats(self): return Scissor()
    @property
    def looses(self): return Paper()


class Paper(Symbol):
    value = 2

    @property
    def beats(self): return Rock()
    @property
    def looses(self): return Scissor()


class Scissor(Symbol):
    value = 3

    @property
    def beats(self): return Paper()
    @property
    def looses(self): return Rock()


with open("input.txt") as file:
    score_total = 0
    for line in file.readlines():
        line = line.strip('\n')
        other, own = (Symbol.create(n) for n in line.split(" "))
        score = own.against(other) + own.offset
        score_total += score
        print(f"total: {score_total}, round_score: {score}, win: {own.against(other)}, base: {own.offset}, ({own} vs. {other})")


with open("input.txt") as file:
    score_total = 0
    for line in file.readlines():
        line = line.strip('\n')
        other_string, own_string = line.split()
        other = Symbol.create(other_string)
        own = other.create_response(own_string)
        score = own.against(other) + own.value
        score_total += score
        print(f"total: {score_total}, round_score: {score}, win: {own.against(other)}, base: {own.value}, ({own} vs. {other})")


print(score_total)
