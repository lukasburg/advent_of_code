from collections import defaultdict


with open("input") as file:
    inp = file.read()


class DefaultDict(defaultdict):
    def __missing__(self, key):
        value = self.default_factory(key)
        self[key] = value
        return value


preprocessed = DefaultDict(lambda time: population(time))


total_time = 256
start_fish = [int(i) for i in inp.split(',')]
# fish = start_fish
# values = []
# for i in range(total_time):
#     fish = [a for tup in [[it-1] if it-1 >= 0 else [6, 8] for it in fish] for a in tup]
#     values.append(len(fish))
#     # print(fish)


def population(time, start_value=None):
    if start_value:
        time = time + (7 - start_value - 1)
    if time < 7:
        return 1
    else:
        return preprocessed[time - 7] + preprocessed[time - 9]


recursive_values = [(start_value, population(total_time, start_value)) for start_value in start_fish]
total_recursive_sum = sum([population(total_time, start_value) for start_value in start_fish])
# print('bad', values)
print('recursive', total_recursive_sum)
