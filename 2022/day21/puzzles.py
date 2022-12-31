import re

from sympy import symbols, Eq, solve

with open("input") as file:
    inp = file.readlines()

number_monkey_parser = re.compile('(\w+): (\d+)')
operation_monkey_parser = re.compile('(\w+): (\w+) ([-*+/]) (\w+)')
PART_TWO = True


class Monkey:
    def __init__(self, name: str):
        self.name = name
        self._value = None

    @property
    def value(self):
        return None

    def __repr__(self):
        return f'{self.name}: {self.__class__.__name__}'

    @classmethod
    def parse_monkey(cls, line):
        nr_match = number_monkey_parser.match(line)
        if number_monkey_parser.match(line):
            name, nr = nr_match.groups()
            return NumberMonkey(name, int(nr))
        else:
            name, first, operation, second = operation_monkey_parser.match(line).groups()
            return OperationMonkey(name, operation, first, second)


class NumberMonkey(Monkey):
    def __init__(self, name, value):
        super().__init__(name)
        self._value = value
        if PART_TWO and self.name == 'humn':
            self._value = symbols('humn')

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
        if PART_TWO and self.name == 'root':
            first = self.first_operand.value
            second = self.second_operand.value
            expr = Eq(first, second)
            print(expr)
            return solve(expr, 'humn')
        self._calculate_own_value()
        return self._value

    def _calculate_own_value(self):
        if self.operation == '*':
            self._value = self.first_operand.value * self.second_operand.value
        elif self.operation == '+':
            self._value = self.first_operand.value + self.second_operand.value
        elif self.operation == '/':
            self._value = self.first_operand.value / self.second_operand.value
        elif self.operation == '-':
            self._value = self.first_operand.value - self.second_operand.value


monkey_dict = dict()
operation_monkeys_need_update = set()
for line in inp:
    monkey = Monkey.parse_monkey(line)
    if isinstance(monkey, OperationMonkey):
        operation_monkeys_need_update.add(monkey)
    monkey_dict[monkey.name] = monkey


for operation_monkey in operation_monkeys_need_update:
    operation_monkey.update_operands_to_instances_from_name(monkey_dict)


# print(monkey_dict['root'].solution_part_two())


print(monkey_dict['root'].value)
# print(monkey_dict['root'].solution_part_two())
