import re
import time
from multiprocessing import Pool

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
RESOURCES = {ORE: 'ore', CLAY: 'clay', OBSIDIAN: 'obsidian', GEODE: 'geode'}

class BotCount(list):
    def __init__(self, build_order):
        self.bot_count = [build_order.count(i) for i in range(4)]
        super().__init__(self.bot_count)

    def __str__(self):
        return f"Bots(" + ", ".join([f"{i}: {self[k]}" for k, i in RESOURCES.items()]) + ")"

class ResourceCount(list):
    def __init__(self, build_order, blueprint):
        build_order = reversed(build_order)
        res = [blueprint.costs[ORE][ORE],0,0,0] # "Refund" costs of first ore bot, you start with 1
        for t, bot in enumerate(build_order):
            if bot is None:
                continue
            res[bot] += t
            for type_, amount in enumerate(blueprint.costs[bot]):
                res[type_] -= amount
        super().__init__(res)
    
    def __str__(self):
        return f"Resources(" + ", ".join([f"{i}: {self[k]}" for k, i in RESOURCES.items()]) + ")"


class BuildOrder(list):
    def __str__(self):
        bo = ', '.join([RESOURCES[self[i]] if self[i] is not None else '_' for i in range(len(self))])
        return f"BuildOrder({bo})"


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
        costs = [
            {ORE: ore_robot_cost}, # ORE:
            {ORE: clay_robot_cost}, # CLAY:
            {ORE: obsidian_robot_ore_cost, CLAY: obsidian_robot_clay_cost}, # OBSIDIAN:
            {ORE: geode_robot_ore_cost, OBSIDIAN: geode_robot_obsidian_cost} # GEODE:
        ]
        self.costs = [
            [costs[i][j] if j in costs[i] else 0 for j in range(4)] for i in range(4)
        ]
        self.max_needed_bots = [
            max([self.costs[bot][ORE] for bot in range(1, 4)]),
            self.costs[OBSIDIAN][CLAY],
            self.costs[GEODE][OBSIDIAN],
        ]

    def __repr__(self):
        return (f"BP{self.number}: ore(ore: {self.costs[ORE][ORE]}), clay(ore: {self.costs[CLAY][ORE]}), "
                f"obsidian(ore: {self.costs[OBSIDIAN][ORE]}, clay: {self.costs[OBSIDIAN][CLAY]}), "
                f"geode(ore: {self.costs[GEODE][ORE]}, obsidian: {self.costs[GEODE][OBSIDIAN]})")


def can_buy(available_resources: ResourceCount, bot_costs):
    for current_resource, amount in enumerate(bot_costs):
        if amount > available_resources[current_resource]:
            return False
    return True


def all_plausible_build_options(res: ResourceCount, blueprint: Blueprint, bot_count, depth, max_depth) -> set[int]:
    can_buy_bots = {
        bot for bot in range(4) if can_buy(res, blueprint.costs[bot])
    }
    if depth == max_depth:
        return {GEODE} if GEODE in can_buy_bots else {None}
    if bot_count[CLAY] == 0:
        # if no clay bots build
        if not ORE in can_buy_bots or not CLAY in can_buy_bots:
            # and can not build both ore and clay, waiting for either might make sense
            can_buy_bots.add(None)
    elif bot_count[OBSIDIAN] == 0:
        # if no obsidian bots and can not build one of the three, waiting for one of them might make sense
        if not {ORE, CLAY, OBSIDIAN}.issubset(can_buy_bots):
            can_buy_bots.add(None)
    elif not {ORE, CLAY, OBSIDIAN, GEODE} == can_buy_bots:
        # bot count obs and clay are both more than one, waiting on any bot might make sense
        can_buy_bots.add(None)
    for res in range(3):
        if res in can_buy_bots and bot_count[res] >= blueprint.max_needed_bots[res]:
            can_buy_bots.remove(res)
    return can_buy_bots


def parse(string) -> list[Blueprint]:
    bp_matcher = "[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*(\\d+)[^\\d]*"
    return [Blueprint(*list(map(int, re.match(bp_matcher, line).groups()))) for line in string.split("\n")]


def highest_possible_geode_number(build_order, blueprint, max_depth):
    missing_count = max_depth - len(build_order)
    max_geode = build_order + ([GEODE] * missing_count)
    return ResourceCount(max_geode, blueprint)[GEODE]


def recursive_options_search(previous_bo, blueprint, max_depth, progress_dict, is_waiting_for_other_bot=False, possible_before=None):
    if possible_before is None:
        possible_before = set()

    if DEBUG:
        progress_dict['prog'] += 1
    #     if PROGRESS['prog'] % 100000 == 0:
    #         print(f"[{blueprint.number}] Checked {PROGRESS['prog']} | Current BO: {BuildOrder(previous_bo)}")

    depth = len(previous_bo)
    if depth >= max_depth:
        # STOP IF TIME IS max_depth (24/32)
        score = ResourceCount(previous_bo, blueprint)[GEODE]
        if DEBUG:
            if score > progress_dict['max_score']:
                progress_dict['max_score'] = score
                print(f"[{blueprint.number}] New max score: {score} with {BuildOrder(previous_bo)}")
        return score

    if highest_possible_geode_number(previous_bo, blueprint, max_depth) <= progress_dict['max_score']:
        # stop evaluating if beating highest score is no longer possible
        return 0

    scores = [0]
    options = all_plausible_build_options(ResourceCount(previous_bo, blueprint), blueprint,
                                          BotCount(previous_bo), depth, max_depth)
    if is_waiting_for_other_bot:
        # if decided to wait before despite being able to build a bot, don't build that bot now, would make sense
        options = options.difference(possible_before)
    for option in options:
        if option is None and len(options) > 1:
            # could build a bot but decided to wait
            possible_before_new = options.difference({None}).union(possible_before)
            scores.append(recursive_options_search(previous_bo + [option], blueprint, max_depth, progress_dict,
                                                   is_waiting_for_other_bot=True, possible_before=possible_before_new))
        else:
            scores.append(recursive_options_search(previous_bo + [option], blueprint, max_depth, progress_dict))

    if DEBUG:
        if progress_dict['deepest'] > len(previous_bo):
            progress_dict['deepest'] = len(previous_bo)
            progress_pseudo_percent = (max_depth-len(previous_bo)) / max_depth
            print(f"[{blueprint.number}] ('{progress_pseudo_percent:.2%}') "
                  f"Deepest subtree finished ({progress_dict['deepest']}) after: {progress_dict['prog']}")

    return max(scores)

def options_search_wrapper(blueprint):
    progress = {'deepest': 99, 'max_score': 0, 'prog': 0}
    start_time = time.time()
    res =  blueprint.number, recursive_options_search([ORE], blueprint, 25, progress)
    total_time = time.time() - start_time
    if DEBUG:
        print('############')
        print(f"[{blueprint.number}] Took {total_time:.2f}s to complete")
        print('############')
    return res

def options_search_wrapper2(blueprint):
    progress = {'deepest': 99, 'max_score': 0, 'prog': 0}
    start_time = time.time()
    res =  blueprint.number, recursive_options_search([ORE], blueprint, 33, progress)
    total_time = time.time() - start_time
    if DEBUG:
        print('############')
        print(f"[{blueprint.number}] Took {total_time:.2f}s to complete")
        print('############')
    return res

def quality(b):
    return b[0] * b[1]

sample_bo = [ORE,
      None, None, CLAY, None, CLAY,
      None, CLAY, None, None, None,
      OBSIDIAN, CLAY, None, None, OBSIDIAN,
      None, None, GEODE, None, None,
      GEODE, None, None, None]

def run(file="input.txt"):
    blueprints = parse(read(file))
    # for bp in blueprints:
    #     print(bp)
    #     bo = [ORE]
    #     print(recursive_options_search(bo, bp))
    #     break
    with Pool(4) as pool:
        result = pool.map(options_search_wrapper, blueprints)
        # print(result)
        qualities = list(map(quality, result))
        print("Qualities: ", qualities)
        return sum(qualities)

def product_part_two(max_geodes):
    total = 1
    for _, p in max_geodes:
        total *= p

def run2(file="input.txt"):
    blueprints = parse(read(file))[:3]
    # for bp in blueprints:
    #     print(bp)
    #     bo = [ORE]
    #     print(recursive_options_search(bo, bp))
    #     break
    with Pool(3) as pool:
        result = pool.map(options_search_wrapper2, blueprints)
        # print(result)
        qualities = result
        print("Qualities: ", qualities)
        return product_part_two(qualities)


if __name__ == "__main__":
    DEBUG = True
    # print(run("example.txt"))
    print(run2())
