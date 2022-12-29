import re

with open("input") as file:
    inp = file.readlines()

number_monkey_parser = re.compile('(\w+): (\d+)')
operation_monkey_parser = re.compile('(\w+): (\w+) ([-*+/]) (\w+)')


class Monkey:
    def __init__(self, name: str):
        self.name = name
        self._value = None

    @property
    def value(self):
        return None

    @classmethod
    def parse_monkey(cls, line, humans_for_part_two=False):
        nr_match = number_monkey_parser.match(line)
        if number_monkey_parser.match(line):
            name, nr = nr_match.groups()
            if name == 'humn' and humans_for_part_two:
                return Human(name, None)
            return NumberMonkey(name, int(nr))
        else:
            name, first, operation, second = operation_monkey_parser.match(line).groups()
            if name == 'root':
                return RootMonkey(name, operation, first, second)
            else:
                return OperationMonkey(name, operation, first, second)


class NumberMonkey(Monkey):
    def __init__(self, name, value):
        super().__init__(name)
        self._value = value

    @property
    def value(self):
        return self._value


class OperationMonkey(Monkey):
    def __init__(self, name, operation, first: str, second: str):
        super().__init__(name)
        self.operation = operation
        self.first_str = first
        self.second_str = second
        self.first_operand: Monkey = None
        self.second_operand: Monkey = None

    def update_operands_to_instances_from_name(self, monkey_dict: dict[str, Monkey]):
        self.first_operand = monkey_dict[self.first_str]
        self.second_operand = monkey_dict[self.second_str]

    @property
    def value(self):
        return self._calculate_own_value()

    def _calculate_own_value(self):
        if self.operation == '*':
            self._value = self.first_operand.value * self.second_operand.value
        elif self.operation == '+':
            self._value = self.first_operand.value + self.second_operand.value
        elif self.operation == '/':
            self._value = self.first_operand.value // self.second_operand.value
        elif self.operation == '-':
            self._value = self.first_operand.value - self.second_operand.value

    def solve_for(self, should_be_value):
        first, second = None, None
        try:
            first = self.first_operand.value
        except PunyHumanException:
            pass
        try:
            second = self.first_operand.value
        except PunyHumanException:
            pass
        if self.operation == '+':
            if first:  # known + ??? = should ->  ??? = should - known
                second_should_have_value = should_be_value - first
                return self.second_operand.solve_for(second_should_have_value)
            elif second:
                first_should_have_value = should_be_value - second
                return self.first_operand.solve_for(first_should_have_value)
            else:  # ??? + ??? = should
                first = self.first_operand.solve_for(should_be_value)
                second = self.second_operand.solve_for(should_be_value)
                first_fraction = first // (first + second)
                second_fraction = second // (first + second)
                assert self.first_operand.solve_for(first_fraction) == self.second_operand.solve_for(second_fraction)
                return self.first_operand.solve_for(first_fraction)
        if self.operation == '*':
            if first:  # known * ??? = should ->  ??? = should / known
                second_should_have_value = should_be_value // first
                return self.second_operand.solve_for(second_should_have_value)
            elif second:
                first_should_have_value = should_be_value // second
                return self.first_operand.solve_for(first_should_have_value)
            else:  # ??? - ??? = should
                first = self.first_operand.solve_for(should_be_value)
                second = self.second_operand.solve_for(should_be_value)

        if self.operation == '-':
            if first:  # first - ??? = should ->  ??? = first - should
                second_should_have_value = first - should_be_value
                return self.second_operand.solve_for(second_should_have_value)
            elif second:  # ??? - second = should ->  ??? = should + second
                first_should_have_value = should_be_value + second
                return self.first_operand.solve_for(first_should_have_value)
        if self.operation == '/':
            if first:  # first / ??? = should ->  ??? = first / should
                second_should_have_value = first // should_be_value
                return self.second_operand.solve_for(second_should_have_value)
            elif second:  # ??? / second = should ->  ??? = should * second
                first_should_have_value = should_be_value * second
                return self.first_operand.solve_for(first_should_have_value)


# Part 2
class RootMonkey(OperationMonkey):
    def solution_part_two(self):
        first_value = None
        second_value = None
        try:
            first_value = self.first_operand.value
        except PunyHumanException:
            print('First value unknown')
        try:
            second_value = self.second_operand.value
        except PunyHumanException:
            print('First value unknown')
        print(first_value, second_value)
        known = first_value if first_value else second_value
        unknown = self.first_operand if not first_value else self.second_operand
        return unknown.solve_for(known)


class PunyHumanException(Exception):
    pass


class Human(NumberMonkey):
    @property
    def value(self):
        raise PunyHumanException('This human is still figuring out, which value to yell')

    def should_be_value(self, value):
        return value


monkey_dict = dict()
operation_monkeys_need_update = set()
for line in inp:
    monkey = Monkey.parse_monkey(line, humans_for_part_two=True)
    if isinstance(monkey, OperationMonkey):
        operation_monkeys_need_update.add(monkey)
    monkey_dict[monkey.name] = monkey


for operation_monkey in operation_monkeys_need_update:
    operation_monkey.update_operands_to_instances_from_name(monkey_dict)


print(monkey_dict['root'].solution_part_two())
