import math

with open('input') as file:
    inp = file.readlines()

symbols = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}


def parse_snafu(string):
    number = 0
    for index, letter in enumerate(reversed(string)):
        number += int(symbols[letter]) * (5**index)
    return number


total_sum = 0
for line in inp:
    total_sum += parse_snafu(line.strip())
    # print(f'{line.strip()}: {number}')
print(f'Total sum in base 10: {total_sum}')


max_exponent = int(math.log(total_sum, 5)) + 1
reversed_snafu = ''
remaining_sum = total_sum
for i in reversed(range(max_exponent+1)):
    min_total_next = (-3*5**(i-1))
    max_total_next = (3*5**(i-1))
    current_power = 5 ** i
    for x in [2, 1, 0, -1, -2]:
        next_total = remaining_sum - x * current_power
        if (min_total_next <= next_total <= max_total_next and
               abs(next_total) < abs(remaining_sum - (x-1) * current_power)):  # next x isn't closer
            break
    else:
        print(f'No fitting number found (i={i})')
    symbol = [key for key, num in symbols.items() if num == x]
    reversed_snafu += symbol[0]
    remaining_sum = next_total

print(f'{total_sum} as snafu: {reversed_snafu} and parsed back to double check: {parse_snafu(reversed_snafu)}')
print()
