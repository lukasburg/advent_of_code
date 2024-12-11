import re
from itertools import product
from random import shuffle

RESOURCES = [None, 'ore', 'clay', 'obsidian', 'geode']

def read(filename="input.txt"):
    with open(filename) as file:
        return file.read()[:-1]

class Blueprint:
    def __init__(self, number,
                 ore_robot_cost,
                 clay_robot_cost,
                 obsidian_robot_ore_cost,
                 obsidian_robot_clay_cost,
                 geode_robot_ore_cost,
                 geode_robot_obsidian_cost):
        self.number = number
        self.costs = {
            None: dict(),
            'ore': {'ore': ore_robot_cost},
            'clay': {'ore': clay_robot_cost},
            'obsidian': {'ore': obsidian_robot_ore_cost, 'clay': obsidian_robot_clay_cost},
            'geode': {'ore': geode_robot_ore_cost, 'obsidian': geode_robot_obsidian_cost},
        }

    def __repr__(self):
        return (f"BP{self.number}: ore(ore: {self.costs['ore']}), clay(ore: {self.costs['clay']}), "
                f"obsidian({self.costs['obsidian']}), "
                f"geode({self.costs['geode']})")

def parse(string):
    bp_matcher = "[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*"
    return [Blueprint(*list(map(int, re.match(bp_matcher, line).groups()))) for line in string.split("\n")]

def internal_generator(options, repeat=1):
    def cycle(values, uplevel):
        shuffle(values)
        for prefix in uplevel:       # cycle through all upper levels
            for current in values:   # restart iteration of current level
                if current in (None, 'clay', 'ore'):
                    yield prefix + (current, )
                if current == 'obsidian' and 'clay' in prefix:
                    yield prefix + (current, )
                if current == 'geode' and 'obsidian' in prefix:
                    yield prefix + (current, )

    stack = (),
    for level in (options, ) * repeat:
        stack = cycle(level, stack)  # build stack of iterators
    return stack

def build_order_generator() -> product:
    repeat = 23
    for bo in internal_generator(RESOURCES, repeat):
        if 'geode' in bo:
            yield tuple(['ore']) + bo + tuple([None])

def calc_amount_of_resources_at_time(blueprint, build_order, time):
    build_until_now = list(reversed(build_order[:time]))
    # print(list(build_until_now))
    resources = {res: 0 for res in RESOURCES}
    for t, bot in enumerate(build_until_now, 1):
        resources[bot] += t
        if t != time:
            for resource, amount in blueprint.costs[bot].items():
                resources[resource] -= amount
    # del resources[None]
    return resources

def check_validity(blueprint, build_order):
    for t in range(25):
        resources = calc_amount_of_resources_at_time(blueprint, build_order, t)
        # print(t, resources)
        for res in resources.values():
            if res < 0:
                return False
    return True

def run(file):
    for bp in parse(read(file)):
        print(bp)
        max_geode_count = 0
        for i, bo in enumerate(build_order_generator()):
            if i % 100000 == 0:
                print(f"{i}/{pow(5, 23)}")
                print(bo)
            # purge if geode count = 0 or smaller than current max
            geode_count = calc_amount_of_resources_at_time(bp, bo, 24)['geode']
            # print(calc_amount_of_resources_at_time(bp, bo, 25))
            if geode_count == 0 or geode_count < max_geode_count:
                continue
            if check_validity(bp, bo):
                print(f"new max: {geode_count} with build order")
                print(bo)
                max_geode_count = geode_count
        break

if __name__ == "__main__":
    run("example.txt")
    # run("input.txt")
