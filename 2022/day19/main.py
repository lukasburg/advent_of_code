import re
import itertools
from itertools import product
from typing import Tuple


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
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_robot_ore_cost = obsidian_robot_ore_cost
        self.obsidian_robot_clay_cost = obsidian_robot_clay_cost
        self.geode_robot_ore_cost = geode_robot_ore_cost
        self.geode_robot_obsidian_cost = geode_robot_obsidian_cost

    def __repr__(self):
        return (f"BP{self.number}: ore(ore: {self.ore_robot_cost}), clay(ore: {self.clay_robot_cost}), "
                f"obsidian(ore: {self.obsidian_robot_ore_cost}, clay: {self.obsidian_robot_clay_cost}), "
                f"geode(ore: {self.geode_robot_ore_cost}, obsidian: {self.geode_robot_obsidian_cost})")

def parse(string):
    bp_matcher = "[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*"
    return [Blueprint(*list(map(int, re.match(bp_matcher, line).groups()))) for line in string.split("\n")]

def build_order_generator() -> product[tuple[str | None, ...]]:
    options = [None, 'ore', 'clay', 'obsidian', 'geode']
    return itertools.product(options, repeat=23)

def calc_amount_of_resources_at_time(build_order, time):
    build_until_now = reversed(build_order[:time])


def run(file):
    for bp in parse(read(file)):
        print(bp)
        for i, bo in enumerate(build_order_generator()):
            print(bo)
            if i >= 100:
                break

if __name__ == "__main__":
    run("example.txt")
    # run("input.txt")
