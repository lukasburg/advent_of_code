with open("input") as file:
    inp = file.readlines()

x, y = 0, 0
for line in inp:
    if line.startswith('forward'):
        x += int(line.split(' ')[1])
    if line.startswith('down'):
        y += int(line.split(' ')[1])
    if line.startswith('up'):
        y -= int(line.split(' ')[1])

print(x*y)


x2, y2, aim = 0, 0, 0
for line in inp:
    if line.startswith('forward'):
        value = int(line.split(' ')[1])
        x2 += value
        y2 += aim*value
    if line.startswith('down'):
        aim += int(line.split(' ')[1])
    if line.startswith('up'):
        aim -= int(line.split(' ')[1])

print(x2*y2)
