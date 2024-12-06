import itertools
import operator
from functools import reduce

import numpy as np


with open('input') as file:
    inp = file.read()


class Ruleset:
    def __init__(self, string_input):
        self.rules = []
        self.targets = []
        self._parse_rule(string_input)
        self.rules_as_complete_string = f"[{','.join(self.rules)}]"

    def get_target(self, part: 'Part'):
        parsed = eval(self.rules_as_complete_string, part.ratings)
        first_match = parsed.index(True)
        return self.targets[first_match]

    def get_mins_maxes(self):
        return [self._get_min_max(i) for i in range(len(self.rules))]

    def _get_min_max(self, index_of_rule) -> tuple[str, tuple[int, int], str]:
        rule = self.rules[index_of_rule]
        target = self.targets[index_of_rule]
        if '<' in rule:
            attribute, value = rule.split('<')
            return attribute, (0, int(value) - 1), target
        if '>' in rule:
            attribute, value = rule.split('>')
            return attribute, (int(value) + 1, 4000), target
        return 'x', (0, 4000), target

    def __str__(self):
        return f"{self.name}{{" + ', '.join([f"{self.rules[i]}: {self.targets[i]}" for i in range(len(self.rules))]) + "}"

    def _parse_rule(self, string_input):
        name, rest = string_input.split('{')
        self.name = name
        for pair in rest.replace('}', ':').split(','):
            rule, target = pair.split(':')
            if target:
                self.rules.append(rule)
                self.targets.append(target)
            else:
                self.rules.append('True')
                self.targets.append(rule)


class Part:
    variable_names = {'x': 'x', 'm': 'm', 'a': 'a', 's': 's'}

    def __init__(self, string_input):
        self.ratings = eval(string_input.replace('=', ':'), self.variable_names)
        self.score = sum(self.ratings.values())

    def run_trough(self, current_rule_name: str, rules: dict[str, Ruleset]):
        next_rule = rules[current_rule_name].get_target(self)
        if next_rule == 'A':
            return True, current_rule_name
        elif next_rule == 'R':
            return False, current_rule_name
        else:
            return *self.run_trough(next_rule, rules), current_rule_name


def parse_input(string_input: str) -> (list[Part], dict[str, Ruleset]):
    rule_lines, part_lines = string_input.split('\n\n')
    parts = []
    rules = dict()
    for part_line in part_lines[:-1].split('\n'):
        part = Part(part_line)
        parts.append(part)
    for rule_line in rule_lines.split('\n'):
        rule = Ruleset(rule_line)
        rules[rule.name] = rule
    return parts, rules


def run(string_input: str):
    parts, rules = parse_input(string_input)
    total_sum = 0
    for part in parts:
        path = part.run_trough('in', rules)
        if path[0]:
            total_sum += part.score
    print(total_sum)
    return rules


# Second part
MinMaxValues = dict[str, tuple[int, int]]


def is_valid_values_set(values: MinMaxValues) -> bool:
    for min_value, max_value in values.values():
        if min_value > max_value:
            return False
    return True


def render_values(values: MinMaxValues) -> str:
    rendered = ', '.join([f"{min_max[0]}<{attr}<{min_max[1]}" for attr, min_max in values.items()
                          if min_max[0] > 0 or min_max[1] < 4000])
    return f"{{{rendered}}}"


def values_overlap(values_one: MinMaxValues, values_two: MinMaxValues):
    for attr_name in values_one:
        min1, max1 = values_one[attr_name]
        min2, max2 = values_two[attr_name]
        if (min1 > max2) or (max1 < min2):
            return False
    return True


def valid_values(acceptable_values: list[MinMaxValues]):
    total_variations = 0
    for acceptables in acceptable_values:
        ranges = map(lambda k: k[1] - k[0], acceptables.values())
        product = reduce(operator.mul, ranges)
        total_variations += product
    return total_variations
    # x = np.empty(shape=[4000, 4000, 4000], dtype=np.int8)
    # print(x.shape)


def run_part_two(rulesets: dict[str, Ruleset]):
    start = rulesets['in']
    start_values = {'x': (0, 4000), 'm': (0, 4000), 'a': (0, 4000), 's': (0, 4000),}
    at_rules = [(start, start_values)]
    i = 0
    acceptable_values: list[MinMaxValues] = []
    while at_rules:
        i += 1
        new_at_rules = []
        # print(f"\nStarting round {i}:")
        for ruleset, values in at_rules:
            for attribute, min_max, target in ruleset.get_mins_maxes():
                new_values = values.copy()
                new_min, new_max = min_max
                new_values[attribute] = (max(values[attribute][0], new_min), min(values[attribute][1], new_max))
                if target == 'A':
                    # print(f"Found acceptable value set {render_values(new_values)} from {ruleset} to 'A'")
                    acceptable_values.append(new_values)
                elif target == 'R':
                    # print(f"Discard from {ruleset} to R")
                    continue
                else:
                    new_ruleset = rulesets[target]
                    if is_valid_values_set(new_values):
                        new_at_rules.append((new_ruleset, new_values))
                        # print(f"From {ruleset} with {render_values(values)} to"
                        #       f" {new_ruleset.name} with {render_values(new_values)}")
                    else:
                        pass
                        # print(f"Discard from {ruleset} to {new_ruleset.name} with {render_values(new_values)}")
        at_rules = new_at_rules
    print(f'All paths finished after {i} steps, found a total of {len(acceptable_values)} valid sets')
    print(acceptable_values)
    print(valid_values(acceptable_values))


if __name__ == "__main__":
    # print(values_overlap({'a': (0, 10), 'b': (0, 3)}, {'a': (5, 12), 'b': (2, 5)}))
    run_part_two(run(inp))
