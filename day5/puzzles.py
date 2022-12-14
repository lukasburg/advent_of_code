import re

with open("inpureversedt.txt") as file:
    containers = ''
    while (line := file.readline()).strip():
        containers += line
    instructions = file.readlines()

rowed_containers = containers.split('\n')
rows = [list(row[1:-1:4]) for row in rowed_containers[:-2]]
cols = [[] for i in range(len(rows[0])+1)]
for row in reversed(rows):
    for col_index, symbol in enumerate(row):
        if symbol != ' ':
            # add one empty column at beginning, because instructions are 1-base indexed
            cols[col_index+1].append(symbol)

matcher = re.compile('move (.+?) from (.+?) to (.+?)')
for instruction in instructions:
    amount, start, destination = [int(i) for i in matcher.search(instruction).groups()]
    # get moving containers
    moved_containers = cols[start][-amount:]
    # paste them in reverse order for puzzle 1
    # cols[destination] += reversed(moved_containers)
    cols[destination] += moved_containers
    # remove moved containers
    cols[start] = cols[start][:-amount]

print(cols)
print(''.join([col[-1] for col in cols[1:]]))
