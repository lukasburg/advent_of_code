from re import findall

line = ""

with open("input") as file:
    line = file.read()


muls = findall("mul\\((\\d{1,3}),(\\d{1,3})\\)|(do\\(\\))|(don't\\(\\))", line)

sum = 0
state = True
for a, b, c, d in muls:
    if c == "do()":
        state = True
    elif d == "don't()":
        state = False
    else:
        if state:
            prod = int(a) * int(b)
            sum = prod + sum


print(sum)
