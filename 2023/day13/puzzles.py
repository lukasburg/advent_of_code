# h and v are named confusingly. h is actually a vertical line, while v is actually a horizontal line

with open("input") as file:
    inp = file.read()[:-1]


def render(before, after, v=False, h=False):
    if v:
        print('\n'.join(before))
        print('-'*len(pattern[0]))
        print('\n'.join(after))
    if h:
        height = len(before)
        assembled = [before[h] + "|" + after[h] for h in range(height)]
        print('\n'.join(assembled))


def create_parts(pattern, h=None, v=None):
    if v is not None:
        size = min(len(pattern[:v]), len(pattern[v:]))
        before_mirror = pattern[v-size:v]
        after_mirror = pattern[v:v+size]
        # render(before_mirror, after_mirror, v=True)
        return before_mirror, list(reversed(after_mirror))
    if h is not None:
        size = min(len(pattern[0])-h, h)
        before_mirror = [row[h-size:h] for row in pattern]
        after_mirror = [row[h:h+size] for row in pattern]
        # render(before_mirror, after_mirror, h=True)
        rev = [''.join(reversed(row)) for row in after_mirror]
        return before_mirror, rev


def is_reflection(before, after):
    return before == after


def is_reflection_if_smudged(before, after):
    before_set = {(symbol, x, y) for y, row in enumerate(before) for x, symbol in enumerate(row)}
    after_set = {(symbol, x, y) for y, row in enumerate(after) for x, symbol in enumerate(row)}
    return len(before_set.difference(after_set)) == 1


def find_factor(pattern):
    for h in range(1, len(pattern[0])):
        before, after = create_parts(pattern, h=h)
        if is_reflection(before, after):
            return h
    for v in range(1, len(pattern)):
        before, after = create_parts(pattern, v=v)
        if is_reflection(before, after):
            return v*100


def find_factor_with_smudge(pattern):
    for h in range(1, len(pattern[0])):
        before, after = create_parts(pattern, h=h)
        if is_reflection_if_smudged(before, after):
            return h
    for v in range(1, len(pattern)):
        before, after = create_parts(pattern, v=v)
        if is_reflection_if_smudged(before, after):
            return v*100


patterns = inp.split('\n\n')
total = 0
total_smudged = 0
for pattern in patterns:
    pattern = pattern.split('\n')
    total += find_factor(pattern)
    total_smudged += find_factor_with_smudge(pattern)


print(total)
print(total_smudged)
