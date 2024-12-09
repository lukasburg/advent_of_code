import itertools
from copy import copy


def read(filename="input.txt.txt"):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    files = list(map(int, string[::2]))
    spaces = list(map(int, string[1::2]))
    total_list = []
    file_list = []
    file_areas = []
    empty_areas = []
    head_position = 0
    for i, file, space in zip(range(len(files)), files, spaces):
        total_list += [i for _ in range(file)]
        file_list += [i for _ in range(file)]
        file_areas.append((i, range(head_position, head_position+file)))
        head_position += file
        total_list += ['_' for _ in range(space)]
        empty_areas.append(range(head_position, head_position+space))
        head_position += space
    if not len(files) == len(spaces):
        file_areas.append((i+1, range(head_position, head_position+files[-1])))
        file_list += [len(files)-1 for _ in range(files[-1])]
        total_list += [len(files)-1 for _ in range(files[-1])]
    # print(f'[{", ".join(map(str, total_list))}]')
    return file_list, empty_areas, file_areas

def calculate_sum(disk):
    return sum([i*num for i, num in enumerate(disk) if num != "_"])

def find_empty_space(empty_areas, file_index, file_area):
    for e_index, empty_area in enumerate(empty_areas):
        if empty_area.start >= file_area.start: break
        if len(empty_area) >= len(file_area):
            empty_areas[e_index] = range(empty_area.stop - (len(empty_area) - len(file_area)), empty_area.stop)
            return file_index, range(empty_area.start, empty_area.start+len(file_area))
    return file_index, file_area

def run(file):
    disk, empty_areas, file_areas = parse(read(file))
    print("Empty: ", empty_areas)
    print("Files: ", file_areas)
    for area in empty_areas:
        for e in area:
            disk.insert(e, disk.pop())
    print(calculate_sum(disk))
    new_file_areas = []
    for file_index, file_area in reversed(file_areas):
        new_file_areas.append(find_empty_space(empty_areas, file_index, file_area))
    highest_point = max(map(lambda it: it[1].stop, new_file_areas))
    new_disk = ['_' for _ in range(highest_point)]
    for file_index, area in new_file_areas:
        for point in area:
            new_disk[point] = file_index
    # print(f'[{", ".join(map(str, new_disk))}]')
    print(calculate_sum(new_disk))
    # print(new_file_areas)
    # print(disk)

    # print(of_which_empty)

if __name__ == "__main__":
    run("example.txt")
    # run("input.txt")
