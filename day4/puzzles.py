with open("input.txt") as file:
    input_lines = file.readlines()


insides = 0
overlaps = 0
for line in input_lines:
    one, two = [[int(i) for i in pair.split('-')] for pair in line.strip().split(',')]
    is_inside = (one[0] <= two[0] and one[1] >= two[1]) or (one[0] >= two[0] and one[1] <= two[1])
    does_overlap = set(range(one[0], one[1]+1)).intersection(set(range(two[0], two[1]+1)))
    print(one, two, is_inside, bool(does_overlap))
    if does_overlap:
        overlaps += 1
    if is_inside:
        insides += 1


print(insides)
print(overlaps)
