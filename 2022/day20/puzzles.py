with open('input') as file:
    numbers = [int(i) for i in file.readlines()]


class LinkedListItem:
    def __init__(self, value: int, list_len: int):
        self.list_len = list_len-1
        self.value: int = value
        self.prev: LinkedListItem = None
        self.next: LinkedListItem = None

    def __str__(self):
        return f'{self.prev.value}<({self.value})>{self.next.value}'

    def __repr__(self):
        return str(self)

    def move(self):
        move_by = self.value % self.list_len
        if move_by == 0:  # value was 0 or moved exactly in a circle
            return
        else:
            new_pos = self.next
            for i in range(move_by-1):
                new_pos = new_pos.next
        # link gap made by moving self
        self.prev.next = self.next
        self.next.prev = self.prev
        # update new position
        self.prev = new_pos
        self.next = new_pos.next
        # update new neighbors
        new_pos.next = self
        self.next.prev = self


def format_linked_list(linked_list, current=None):
    length = len(linked_list)
    if not current:
        current = linked_list[-1]
    listed_by_order = []
    for i in range(length):
        listed_by_order.append(current.value)
        current = current.next
    return listed_by_order


list_len = len(numbers)
linked_list = [LinkedListItem(number, list_len) for number in numbers]
for i in range(list_len):
    if linked_list[i].value == 0:
        zero = linked_list[i]
    linked_list[i].next = linked_list[(i+1)%list_len]
    linked_list[i].prev = linked_list[i-1]


for number in linked_list:
    # print(format_linked_list(linked_list, zero))
    # print(f'Moving {number.value}')
    number.move()


ordered_list = format_linked_list(linked_list, zero)
# print([ordered_list[index] for index in [1000, 2000, 3000]])
print([ordered_list[index % list_len] for index in [1000, 2000, 3000]])
print(sum([ordered_list[index % list_len] for index in [1000, 2000, 3000]]))


with open('output', 'w') as file:
    for number in ordered_list:
        file.write(str(number) + '\n')


#
# Second part
#

key = 811589153
linked_list = [LinkedListItem(number * key, list_len) for number in numbers]
for i in range(list_len):
    if linked_list[i].value == 0:
        zero = linked_list[i]
    linked_list[i].next = linked_list[(i+1)%list_len]
    linked_list[i].prev = linked_list[i-1]

for i in range(10):
    for number in linked_list:
        number.move()


ordered_list = format_linked_list(linked_list, zero)
print([ordered_list[index % list_len] for index in [1000, 2000, 3000]])
print(sum([ordered_list[index % list_len] for index in [1000, 2000, 3000]]))
