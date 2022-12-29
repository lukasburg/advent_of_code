import re
from collections import defaultdict
from itertools import chain

with open('example-input') as file:
    inp = file.readlines()


class Resources:
    def __init__(self, ore=0, clay=0, obsidian=0, geodes=0):
        self.geodes = geodes
        self.obsidian = obsidian
        self.clay = clay
        self.ore = ore

    def __ge__(self, other: 'Resources'):
        return (self.ore >= other.ore and
                self.clay >= other.clay and
                self.obsidian >= other.obsidian and
                self.geodes >= other.geodes)

    def __le__(self, other: 'Resources'):
        return (self.ore <= other.ore and
                self.clay <= other.clay and
                self.obsidian <= other.obsidian and
                self.geodes <= other.geodes)

    def __eq__(self, other: 'Resources'):
        return other.ore == self.ore and other.clay == self.clay and other.obsidian == self.obsidian and other.geodes == self.geodes

    def copy(self):
        return self + Resources()

    def __add__(self, other: 'Resources'):
        return Resources(self.ore + other.ore,
                         self.clay + other.clay,
                         self.obsidian + other.obsidian,
                         self.geodes + other.geodes)

    def __sub__(self, other: 'Resources'):
        return Resources(self.ore - other.ore,
                         self.clay - other.clay,
                         self.obsidian - other.obsidian,
                         self.geodes - other.geodes)

    def __str__(self):
        as_dict = {'ore': self.ore, 'clay': self.clay, 'obsidian': self.obsidian, 'geodes': self.geodes}
        return f"{as_dict}"

    def __getitem__(self, item):
        match item:
            case 'ore': return self.ore
            case 'clay': return self.clay
            case 'obsidian': return self.obsidian
            case 'geode': return self.geodes
        raise KeyError

    def __hash__(self):
        return hash((self.ore, self.clay, self.obsidian, self.geodes))


class ComparableResourceSet:
    def __init__(self):
        self.resource_set = set()

    def is_smaller_than_with_update_if_bigger(self, resources: Resources):
        for own_resource in self.resource_set:
            if resources == own_resource:
                return True
            elif resources <= own_resource:
                return False
            elif resources >= own_resource:
                self.resource_set.remove(own_resource)
                break
        self.resource_set.add(resources.copy())
        return True


class Factory:
    number_matcher = re.compile('(\d+)')

    def __init__(self, index,
                 ore_bot_cost: Resources,
                 clay_bot_cost: Resources,
                 obsidian_bot_cost: Resources,
                 geode_bot_cost: Resources):
        self.costs = {
            'ore': ore_bot_cost,
            'clay': clay_bot_cost,
            'obsidian': obsidian_bot_cost,
            'geode': geode_bot_cost
        }
        self.index = index
        self.max_needed_per_tick = Resources(
            ore=max([clay_bot_cost.ore, obsidian_bot_cost.ore, geode_bot_cost.ore]),
            clay=obsidian_bot_cost.clay,
            obsidian=geode_bot_cost.obsidian,
        )

    def can_build(self, bot_type, available_resources: Resources):
        return available_resources >= self.costs[bot_type]

    @classmethod
    def parse_from_blueprint(cls, string):
        all_numbers = cls.number_matcher.findall(string)
        index, ore_o, c_o, obs_o, obs_c, g_ore, g_obs = [int(i) for i in all_numbers]
        ore_bot_cost = Resources(ore_o)
        clay_bot_cost = Resources(c_o)
        obsidian_bot_cost = Resources(obs_o, clay=obs_c)
        geode_bot_cost = Resources(g_ore, obsidian=g_obs)
        return Factory(index, ore_bot_cost, clay_bot_cost, obsidian_bot_cost, geode_bot_cost)


class Simulation:
    def __init__(self, factory: Factory, verbose=False):
        self.verbose = verbose
        self.bots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
        self.resources = Resources()
        self.factory = factory
        self.build_order = []
        self.in_queue = None

    def _increment_resources(self):
        self.resources += Resources(self.bots['ore'], self.bots['clay'], self.bots['obsidian'], self.bots['geode'])
        if self.verbose:
            print(f'Bots {self.bots} collected resources. You now have {self.resources}')

    def _build(self, bot_type):
        if self.verbose:
            print(f'Start building {bot_type}-collecting robot, spend {self.factory.costs[bot_type]}')
        self.resources -= self.factory.costs[bot_type]
        self.build_order.append(bot_type)
        self.in_queue = bot_type

    def _finish_build(self):
        if self.in_queue:
            self.bots[self.in_queue] += 1
            if self.verbose:
                print(f'The new {self.in_queue}-collecting bot is ready')
            self.in_queue = None

    def _try_to_build(self):
        if self.bots['ore'] < self.factory.max_needed_per_tick.ore:
            if self.factory.can_build('ore', self.resources):
                self._build('ore')
        else:
            if sum([self.factory.can_build('geode', self.resources),
                    self.factory.can_build('clay', self.resources),
                    self.factory.can_build('obsidian', self.resources)]
                   ) > 1 and self.verbose:
                print('Could have build multiple bots! Consider if other build order would have been better?')
            if self.factory.can_build('geode', self.resources):
                self._build('geode')
            elif self.factory.can_build('obsidian', self.resources):
                self._build('obsidian')
            elif self.factory.can_build('clay', self.resources):
                self._build('clay')

    def turn(self):
        self._try_to_build()
        self._increment_resources()
        self._finish_build()

    def __str__(self):
        return f'Bots: {self.bots}, Resources: {self.resources}'

    def simulate_completely(self):
        for i in range(24):
            if self.verbose:
                print(f'\n== Minute {i+1} ==')
            self.turn()
        return self.resources.geodes

    def score(self):
        return self.factory.index * self.resources.geodes

    def bots_hash_string(self):
        return ''.join(f'{k}{v}' for k, v in self.bots.items())


class SimulationByBuildOrder(Simulation):
    def __init__(self, factory, build_order=None, build_next=None, bots=None, resources=None, verbose=False):
        super().__init__(factory, verbose)
        self.build_next = build_next
        self.build_order = build_order if build_order else []
        self.bots = bots if bots else self.bots
        self.resources = resources if resources else self.resources

    def _create_next_build_step_copies(self):
        if not self.build_next:
            copies = [SimulationByBuildOrder(self.factory, self.build_order.copy(), bot_type, self.bots.copy(),
                                             self.resources + Resources(), self.verbose)
                      for bot_type in ('ore', 'clay', 'obsidian', 'geode')
                      if self.bots[bot_type] < self.factory.max_needed_per_tick[bot_type] or bot_type=='geode']
            return copies
        return [self]

    def _try_to_build(self):
        if self.factory.can_build(self.build_next, self.resources):
            self._build(self.build_next)
            self.build_next = None

    def turn_and_return_all_new_build_order_options(self):
        self.turn()
        return self._create_next_build_step_copies()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'Sim(next={self.build_next}, order={self.build_order})'


qualities = []
for i, blueprint in enumerate(inp):
    geodes = Simulation(Factory.parse_from_blueprint(blueprint), verbose=True).simulate_completely()
    quality = geodes*(i+1)
    qualities.append(quality)
    break


print(qualities)
print(sum(qualities))
print('\n\n\n======\n\n\n')


simulations = SimulationByBuildOrder(Factory.parse_from_blueprint(inp[0]))._create_next_build_step_copies()
max_resources_for_current_bots = defaultdict(lambda: ComparableResourceSet())
for i in range(24):
    next_simulations = []
    for sim in simulations:
        next_simulations += sim.turn_and_return_all_new_build_order_options()
    only_bigger_or_equal_simulations = []
    for sim in next_simulations:
        resource_set_for_bot_count = max_resources_for_current_bots[sim.bots_hash_string()]
        if resource_set_for_bot_count.is_smaller_than_with_update_if_bigger(sim.resources):
            only_bigger_or_equal_simulations.append(sim)
    simulations = only_bigger_or_equal_simulations


results = sorted(simulations, key=lambda s: s.score(), reverse=True)[:30]
for result in results:
    print(f'{result.score()}: {". ".join(result.build_order)}')
