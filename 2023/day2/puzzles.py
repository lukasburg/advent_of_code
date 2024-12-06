import re

with open("input") as file:
    inp = file.readlines()


# loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.
total_sum = 0
power_sum = 0
for line in inp:
    g_id = int(re.match("Game (\\d+)", line).groups()[0])
    red = [int(i) for i in re.findall("(\\d+) red", line)]
    blue = [int(i) for i in re.findall("(\\d+) blue", line)]
    green = [int(i) for i in re.findall("(\\d+) green", line)]
    power = max(red)*max(blue)*max(green)
    power_sum += power
    if max(red) > 12 or max(green) > 13 or max(blue) > 14:
        continue
    else:
        total_sum += g_id

print(f"Solution for puzzle 1: {total_sum}")
print(f"Solution for puzzle 2: {power_sum}")
