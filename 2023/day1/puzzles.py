import re

with open("input") as file:
    inp = file.readlines()

total_sum = 0
for line in inp:
    all_digits = re.findall("(\\d)", line)
    first, last = int(all_digits[0]), int(all_digits[-1])
    total_sum += 10*first + last

print(f"Solution to puzzle one: {total_sum}")

string_to_digit = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}
digit_names_for_regex = "|".join(string_to_digit.keys())
total_sum2 = 0
for line in inp:
    # Use ?= (non consuming lookahead) because some string digits overlap)
    all_digits = re.findall(f"(?=(\\d|{digit_names_for_regex}))", line)
    first, last = all_digits[0], all_digits[-1]
    first_as_num = string_to_digit[first] if first in string_to_digit else int(first)
    last_as_num = string_to_digit[last] if last in string_to_digit else int(last)
    line_num = 10*first_as_num + last_as_num
    total_sum2 += line_num

print(f"Solution to puzzle two: {total_sum2}")
