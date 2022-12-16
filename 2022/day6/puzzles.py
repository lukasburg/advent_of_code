with open("input") as file:
    inp = file.read()


def get_start_marker(length):
    for i in range(len(inp)):
        if len(set(inp[i: i+length])) >= length:
            return i+length


print(get_start_marker(4))
print(get_start_marker(14))
