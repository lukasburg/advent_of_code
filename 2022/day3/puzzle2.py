with open("input.txt") as file:
    inp = file.readlines()


print(
    sum(
        [
            range(58)[
                ord(
                    set(elf1.strip()).intersection(set(elf2.strip())).intersection(set(elf3.strip()))
                    .pop()
                )-96]
            for elf1, elf2, elf3
            in [(inp[i], inp[i + 1], inp[i + 2])
                for i in range(0, len(inp), 3)]
        ]
    )
)


# zum (etwas) besseren verständnis hier nochmal imperativ statt funktional
total_value = 0
offset = 96
for elf1, elf2, elf3 in [(inp[i], inp[i + 1], inp[i + 2]) for i in range(0, len(inp), 3)]:
    set1, set2, set3 = set(elf1.strip()), set(elf2.strip()), set(elf3.strip())
    badge = set1.intersection(set2).intersection(set3)
    total_value += range(58)[ord(badge.pop())-offset]

print(total_value)
