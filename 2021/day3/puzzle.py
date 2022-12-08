with open("input") as file:
    inp = file.readlines()


line_count = len(inp)
bit_count = [0 for i in range(12)]
for line in inp:
    for i, symbol in enumerate(line):
        if symbol == '1':
            bit_count[i] += 1


bits = [(amount > line_count/2) for amount in bit_count]
gamma = int(''.join(['1' if i else '0' for i in bits]), 2)
epsilon = int(''.join(['0' if i else '1' for i in bits]), 2)
print(gamma*epsilon)
# print(bit_count, bits)


input_filtered = set(inp)
position = 0
while (remaining_count := len(input_filtered)) > 1:
    ones = sum([1 for line in input_filtered if line[position] == '1'])
    majority = '1' if ones >= remaining_count/2 else '0'
    # print(position, ones, remaining_count, majority)
    input_filtered = set(filter(lambda l: l[position] == majority, input_filtered))
    position += 1

oxygen = int(input_filtered.pop().strip(), 2)


input_filtered = set(inp)
position = 0
while (remaining_count := len(input_filtered)) > 1:
    ones = sum([1 for line in input_filtered if line[position] == '1'])
    minority = '1' if ones < remaining_count/2 else '0'
    # print(position, ones, remaining_count/2, minority)
    input_filtered = set(filter(lambda l: l[position] == minority, input_filtered))
    # print(input_filtered)
    position += 1

co2scrubber = int(input_filtered.pop().strip(), 2)


print(oxygen * co2scrubber)
