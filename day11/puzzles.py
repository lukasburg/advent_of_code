import operator
from functools import reduce
from typing import Callable
import re

Operation = Callable[[int], int]
MonkeyList = list['Monkey']


class Item:
    def __init__(self, start_value):
        self.value = start_value

    def relieve(self):
        self.value = self.value//3
        return self.value

    def modulo_by_common_denominator(self, cd):
        self.value = self.value % cd
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class Monkey:
    numbers = re.compile("\d+")

    def __init__(self,
                 monkey_number: int,
                 start_items: list[Item],
                 operation: Operation,
                 test_divisor: int,
                 target_on_true: int,
                 target_on_false: int):
        self.number = monkey_number
        self.items = start_items
        self.operation = operation
        self.test_divisor = test_divisor
        self.targets = {True: target_on_true, False: target_on_false}
        self.activity = 0

    @classmethod
    def parse(cls, string):
        number_str, items_str, operation_str, divisor_str, true_str, false_str = string.strip().split('\n')
        number = int(cls.numbers.search(number_str).group(0))
        items = [Item(int(i)) for i in cls.numbers.findall(items_str)]
        operation = eval(operation_str.replace('Operation: new =', 'lambda old:'))
        operation.original_string = operation_str.strip()
        divisor = int(cls.numbers.search(divisor_str).group(0))
        target_true = int(cls.numbers.search(true_str).group(0))
        target_false = int(cls.numbers.search(false_str).group(0))
        return cls(number, items, operation, divisor, target_true, target_false)

    def turn(self, monkey_dict: MonkeyList, verbose=False, relieve=True, cd=None):
        self._increment_activity()
        round_stats = []
        for item in self.items:
            start = item.value
            inspect = self._inspect(item)
            current = item.relieve() if relieve else item.modulo_by_common_denominator(cd)
            target, test = self._test_and_throw(item, monkey_dict)
            round_stats.append({'s': start, 'i': inspect, 'c': current, 'm': target, 't': test})
        if verbose:
            self.print_round_info(round_stats, relieve)
        self.items = []

    def print_round_info(self, round_stats, relieve=True):
        print(f'Monkey {self.number}:')
        for stat in round_stats:
            print(f'  Monkey inspects an item with a worry level of {stat["s"]}.')
            print(f'\tWorry level goes to {stat["i"]}.')
            print(f'\tMonkey gets bored with item. '
                  f'Worry level is divided by {"3" if relieve else "common denominator"} to {stat["c"]}.')
            print(f'\tCurrent worry level is {"not " if {stat["t"]} else ""}divisible by {self.test_divisor}.')
            print(f'\tItem with worry level {stat["c"]} is thrown to {stat["m"]}.')

    def catch(self, item: Item):
        self.items.append(item)

    def _increment_activity(self):
        self.activity += len(self.items)

    def _inspect(self, item: Item):
        item.value = self.operation(item.value)
        return item.value

    def _test_and_throw(self, item: Item, monkey_dict: MonkeyList):
        test = item.value % self.test_divisor == 0
        target = self.targets[test]
        monkey_dict[target].catch(item)
        return target, test

    def __str__(self):
        return f'Monkey {self.number}:\n' \
               f'\tItems: {self.items}\n' \
               f'\t{self.operation.original_string}\n' \
               f'\tTest: divisible by {self.test_divisor}\n' \
               f'\tIf True: {self.targets[True]}, If False: {self.targets[False]}'

    def __repr__(self):
        return f'Monkey {self.number}: {self.items}'


with open('input') as file:
    inp = file.read()

ROUNDS = 10000
monkeys = [Monkey.parse(string) for string in inp.split('\n\n')]
common_denominator = reduce(operator.mul, [monkey.test_divisor for monkey in monkeys], 1)
print(common_denominator)

for i in range(ROUNDS):
    for monkey in monkeys:
        monkey.turn(monkeys, verbose=False, relieve=False, cd=common_denominator)
    # print(monkeys)


most_active_two = sorted([monkey.activity for monkey in monkeys])[-2:]
print(most_active_two[0] * most_active_two[1])
