import re
from pprint import pprint

with open('input') as file:
    inp = file.readlines()


def pad_input_with_extra_points(lines):
    bottom_and_top = '.' * (len(lines[0])+2)
    # replace \n in line
    padded_lines = ['.'+line[:-1]+'.' for line in lines]
    return [bottom_and_top] + padded_lines + [bottom_and_top]


padded_input = pad_input_with_extra_points(inp)
part_numbers = []
for line_number, line in enumerate(padded_input):
    matches = [m for m in re.finditer('(\\d+)', line)]
    for match in matches:
        part_above = padded_input[line_number-1][match.start()-1:match.end()+1]
        before, after = line[match.start()-1], line[match.end()]
        part_below = padded_input[line_number+1][match.start()-1:match.end()+1]
        total = part_above + before + after + part_below
        if not re.fullmatch('[.]*', total):
            # print(line_number, total, match)
            part_numbers.append(int(match.group()))
        # else:
            # print(line_number, match)

# pprint(padded_input)
# print(part_numbers)
print(sum(part_numbers))
