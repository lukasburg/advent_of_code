with open("input") as file:
    inp = [int(i.strip()) for i in file.readlines()]

print(sum([1 for a, b in zip(inp[:-1], inp[1:]) if a < b]))

three_window = [a+b+c for a, b, c in zip(inp[:-2], inp[1:-1], inp[2:])]
print(sum([1 for a, b in zip(three_window[:-1], three_window[1:]) if a < b]))
