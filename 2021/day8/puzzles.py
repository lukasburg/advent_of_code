from enum import Enum

with open('input') as file:
    inp = file.readlines()

unique = {2, 3, 4, 7}
print(sum([sum([1 for entry in line.split('|')[1].strip().split() if len(entry) in unique]) for line in inp]))


useful_unique = {2, 3, 4}
# Used pen&paper to come up with this table
solution_for_not_unique_by_hash = {
    (1, 2, 2, 5): 2,
    (1, 2, 3, 5): 5,
    (1, 2, 3, 6): 6,
    (2, 3, 3, 5): 3,
    (2, 3, 3, 6): 0,
    (2, 3, 4, 6): 9,
    (2, 3, 4, 7): 8
}


def hash_number(it_string: set[str], decoded: dict[int, str]):
    it_set = set(it_string)
    similarity1 = len(it_set.intersection(decoded[1]))
    similarity4 = len(it_set.intersection(decoded[4]))
    similarity7 = len(it_set.intersection(decoded[7]))
    return similarity1, similarity7, similarity4, len(it_set)


def decode(symbols):
    uniques = set(filter(lambda k: len(k) in useful_unique, symbols))
    solved = {1 if len(entry) == 2 else 7 if len(entry) == 3 else 4: entry for entry in uniques}
    unsolved_entries = {entry for entry in symbols.difference(uniques)}
    for entry in unsolved_entries:
        entry_hash = hash_number(entry, solved)
        solution = solution_for_not_unique_by_hash[entry_hash]
        solved[solution] = entry
    solution_dict = {item: key for key, item in solved.items()}
    return solution_dict


total_sum = 0
for line in inp:
    first, output = [[''.join(sorted(entry)) for entry in half.strip().split()] for half in line.split('|')]
    solutions = decode(set(first))
    total_sum += sum([solutions[entry]*10**i for i, entry in enumerate(reversed(output))])
print(total_sum)
