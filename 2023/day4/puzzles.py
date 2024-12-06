from collections import defaultdict

with open("input") as file:
    inp = file.readlines()


def parse_line(line):
    return (set([int(nums[i + 1:i + 3]) for i in range(0, len(nums) - 2, 3)])
            for nums in line.split(":")[1].split("|"))


total_points = 0
for line in inp:
    winning, given = parse_line(line)
    matches = len(given.intersection(winning))
    points = pow(2, (matches - 1)) if matches > 0 else 0
    total_points += points

print(total_points)


total_cards = 0
copies = defaultdict(lambda: 1)
for index, line in enumerate(inp):
    winning, given = parse_line(line)
    amount = copies[index]
    matches = len(given.intersection(winning))
    for i in range(index+1, index + matches+1):
        copies[i] = copies[i] + amount

print(sum(copies.values()))
# print(copies)
