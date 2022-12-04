with open("input.txt") as file:
    input = file.readlines()


total_value = 0
offset = 96
for elf1, elf2, elf3 in [(input[i], input[i+1], input[i+2]) for i in range(0, len(input), 3)]:
    set1, set2, set3 = set(elf1.strip()), set(elf2.strip()), set(elf3.strip())
    badge = set1.intersection(set2).intersection(set3)
    total_value += range(58)[ord(badge.pop())-offset]

print(total_value)
