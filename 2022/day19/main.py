import re
from itertools import product
from random import shuffle

RESOURCES = [0, 1, 2, 3, 4]
resource_to_string = {
    None: 0,
    'ore': 1,
    'clay': 2,
    'obsidian': 3,
    'geode': 4
}
# 0 None
# 1 ore
# 2 clay
# 3 obsidian
# 4 geode

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
        self.costs = [
            (),
            ((1, ore_robot_cost), ),
            ((1, clay_robot_cost), ),
            ((1, obsidian_robot_ore_cost), (2, obsidian_robot_clay_cost), ),
            ((1, geode_robot_ore_cost), (3, geode_robot_obsidian_cost), ),
        ]

    def __repr__(self):
        return (f"BP{self.number}: ore(ore: {self.costs[1]}), clay(ore: {self.costs[2]}), "
                f"obsidian({self.costs[3]}), "
                f"geode({self.costs[4]})")

def parse(string):
    bp_matcher = "[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*"
    return [Blueprint(*list(map(int, re.match(bp_matcher, line).groups()))) for line in string.split("\n")]

def internal_generator(options, repeat=1):
    def cycle(values, uplevel):
        shuffle(values)
        for prefix in uplevel:       # cycle through all upper levels
            for current in values:   # restart iteration of current level
                if current in (0, 1, 2):
                    yield prefix + (current, )
                if current == 3 and 2 in prefix:
                    yield prefix + (current, )
                if current == 4 and 3 in prefix:
                    yield prefix + (current, )

    stack = (),
    for level in (options, ) * repeat:
        stack = cycle(level, stack)  # build stack of iterators
    return stack

def build_order_generator() -> product:
    repeat = 23
    for bo in internal_generator(RESOURCES, repeat):
        if 4 in bo:
            yield tuple([1]) + bo + tuple([0])

def calc_amount_of_resources_at_time(blueprint, build_order, time):
    build_until_now = list(reversed(build_order[:time]))
    # print(list(build_until_now))
    resources = [0 for res in RESOURCES]
    for t, bot in enumerate(build_until_now, 1):
        resources[bot] += t
        if t != time:
            for resource, amount in blueprint.costs[bot]:
                resources[resource] -= amount
    # del resources[None]
    return resources

def check_validity(blueprint, build_order):
    for t in range(25):
        resources = calc_amount_of_resources_at_time(blueprint, build_order, t)
        # print(t, resources)
        for res in resources:
            if res < 0:
                return False
    return True

def run(file):
    for bp in parse(read(file)):
        print(bp)
        bo = ('ore', None, None, 'clay', None, 'clay', None, 'clay', None, None, None, 'obsidian', 'clay', None, None,  'obsidian', None, None, 'geode', None, None, 'geode', None, None, None)
        bo = [resource_to_string[it] for it in bo]
        print(calc_amount_of_resources_at_time(bp, bo, 24))
        max_geode_count = 0
        for i, bo in enumerate(build_order_generator()):
            if i % 100000 == 0:
                print(f"{i}/{pow(5, 23)}")
                print(bo)
            # purge if geode count = 0 or smaller than current max
            geode_count = calc_amount_of_resources_at_time(bp, bo, 24)[4]
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
