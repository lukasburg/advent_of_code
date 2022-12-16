with open("input") as file:
    inp = [int(i) for i in file.read().strip().split(',')]


# inp = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
best_height = -1
previous_cost, current_cost = 1000000000, 100000000
while previous_cost > current_cost:
    best_height += 1
    previous_cost = current_cost
    current_cost = sum([abs(i - best_height) for i in inp])
print(previous_cost)


best_height = -1
current_cost = 1000000000000000
previous_cost = current_cost+1
while previous_cost > current_cost:
    best_height += 1
    previous_cost = current_cost
    current_cost = sum([sum(range(1, abs(i - best_height)+1)) for i in inp])
    # print(best_height, current_cost)
print(previous_cost)
