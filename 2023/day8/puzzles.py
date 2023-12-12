import re
from pprint import pprint
from math import lcm

with open('input') as file:
    inp = file.readlines()


class Node:
    def __init__(self, left: str, right: str, name: str):
        self.name = name
        self.left = left
        self.right = right

    def __str__(self):
        return f"N({self.name}, l:{self.left}, r:{self.right})"

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.name)


node_dict = dict()
for line in inp[2:]:
    name, goes_to = line.split("=")
    left, right = re.match(" \\((...), (...)\\)", goes_to).groups()
    node = Node(left, right, name.strip())
    node_dict[name.strip()] = node


def command_list(directions):
    i = -1
    while True:
        i += 1
        command_pos = i % len(directions)
        yield i+1, directions[command_pos], command_pos


# current = node_dict["AAA"]
# for distance, direction, _ in command_list(inp[0][:-1]):
#     next_node = current.left if direction == 'L' else current.right
#     # print(current, direction, next_node)
#     if next_node == "ZZZ":
#         print(f'Reached ZZZ after {distance} steps')
#         break
#     current = node_dict[next_node]


con_current_nodes = list(map(lambda i: i[1], filter(lambda i: i[0].endswith('A'), node_dict.items())))
# all start nodes loop in sync with commands after a certain single point which is also the first reached and node
# probably intentionally
loops_at_and_end_node_at = []
for node in con_current_nodes:
    visited_at = []
    end_nodes_at = set()
    current = node
    command_generator = command_list(inp[0][:-1])
    distance, direction, command_pos = next(command_generator)
    while (current, command_pos) not in visited_at:
        visited_at.append((current, command_pos))
        next_node = current.left if direction == 'L' else current.right
        if next_node.endswith("Z"):
            end_nodes_at.add(distance)
        current = node_dict[next_node]
        distance, direction, command_pos = next(command_generator)
    loop_at = visited_at.index((current, command_pos))
    repetition_loop_length = len(visited_at) - loop_at
    # print(visited_at)
    # print(f"Loop at: {loop_at}. Length of loop: {repetition_loop_length}")
    # print(f"Loop at {current}, command: {command_pos}, d:{distance}")
    print(f"End nodes at {end_nodes_at} and repetitions of {repetition_loop_length}")
    loops_at_and_end_node_at.append(repetition_loop_length)
    # print("---")


solution = lcm(*loops_at_and_end_node_at)
print(f"Destinations reached at: {solution}")
