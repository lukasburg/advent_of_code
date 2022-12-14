from itertools import zip_longest

with open('input') as file:
    inp = file.read()


class WrongOrderException(Exception):
    pass


def compare(left, right, depth=0):
    depth_puffer = "".join(["  " for i in range(depth)])
    print(f'{depth_puffer}- Compare {left} vs {right}')
    if not left and not right:
        return False
    elif not left and not isinstance(left, int):
        print(f"{depth_puffer}  - Left side ran out of items, so inputs are in the right order")
        return True
    elif not right and not isinstance(right, int):
        print(f"{depth_puffer}  - Right side ran out of items, so inputs are not in the right order")
        raise WrongOrderException
    if isinstance(left, list) or isinstance(right, list):
        if not isinstance(left, list) or not isinstance(right, list):
            print(f"{depth_puffer}- Mixed types; convert ... and retry comparison")
        left = [left] if not isinstance(left, list) else left
        right = [right] if not isinstance(right, list) else right
        for left, right in zip_longest(left, right):
            if compare(left, right, depth+1):
                return True
    else:
        if left > right:
            print(f"{depth_puffer}  - Right side is smaller, so inputs are not in the right order")
            raise WrongOrderException
        if left < right:
            print(f"{depth_puffer}  - Left side is smaller, so inputs are in the right order")
        return left < right


def run():
    right_indizes = []
    wrong_order = []
    for index, pair in enumerate(inp.strip().split('\n\n')):
        print(f'\n== Pair {index+1} ==')
        strings = pair.split('\n')
        left, right = eval(strings[0]), eval(strings[1])
        try:
            compare(left, right)
            right_indizes.append(index+1)
        except WrongOrderException:
            wrong_order.append((left, right))
            pass
    print('\nPairs in right order: ', right_indizes, ', sum: ', sum(right_indizes))
    print('\n\n\n===\n\n\n')
    for left, right in wrong_order:
        print()
        try:
            compare(left, right)
        except WrongOrderException:
            pass


run()
