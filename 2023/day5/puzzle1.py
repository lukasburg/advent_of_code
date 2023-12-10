import itertools

with open("example_input") as file:
    inp = file.read()


sections = inp[:-1].split("\n\n")
seeeds = [int(i) for i in sections[0].split(":")[1].split()]
mappers: list[dict[tuple[int, int], int]] = []

for section in sections[1:]:
    # section map is dict like this:    {[source_start, source_end]: shift_by_this_value}
    section_map = dict()
    lines = section.split("\n")
    for line in lines[1:]:
        dest_start, source_start, source_range = [int(num) for num in line.split()]
        section_map[(source_start, source_start + source_range)] = dest_start - source_start
    mappers.append(section_map)


def map_with_map(mapper, number):
    for start, end in mapper.keys():
        if start <= number < end:
            return number+mapper[(start, end)]
    return number


def map_seeed_to_location(seeed, mappers):
    current_result = seeed
    for mapper in mappers:
        current_result = map_with_map(mapper, current_result)
    return current_result


def map_location_to_seeed(seeed, mappers):
    return map_seeed_to_location(seeed, mappers[::-1])


locations = [map_seeed_to_location(seeed, mappers) for seeed in seeeds]
print(f"{min(locations)}")


# to slow :(

# mappers2 = []
# for section in sections[1:]:
#     # section map is dict like this:    {[source_start, source_end]: shift_by_this_value}
#     section_map = dict()
#     lines = section.split("\n")
#     for line in lines[1:]:
#         dest_start, source_start, rang_e = [int(num) for num in line.split()]
#         section_map[(dest_start, dest_start+rang_e)] = source_start - dest_start
#     mappers2.append(section_map)
#
#
# for location in range(10000000000):
#     seeed_at_location = map_location_to_seeed(location, mappers2)
#     if location % 100000 == 0:
#         print(location)
#     if seeed_at_location in seeeds:
#         print(f"Lowest location is {location} at seeed {seeed_at_location}")
#         break
mappers2: list[list[tuple[tuple[int, int], tuple[int, int]]]] = []
for section in sections[1:]:
    # section map is dict like this:    {[source_start, source_end]: shift_by_this_value}
    section_map = []
    lines = section.split("\n")
    for line in lines[1:]:
        dest_start, source_start, source_range = [int(num) for num in line.split()]
        section_map.append((range(source_start, source_start + source_range), range(dest_start, dest_start + source_range)))
    sorted_map = sorted(section_map, key=lambda t: t[0][0])
    mappers2.append(sorted_map)


compressed_mapper = mappers2[0]
for current_mapper in mappers2[1:]:
    new_compressed = []
    for compressed_ranges, current_ranges in itertools.product(compressed_mapper, current_mapper):
        compressed_dest = compressed_ranges[1]
        current_source = current_ranges[0]
        overlap = range(max(compressed_dest[0], current_source[0]), min(compressed_dest[-1], current_source[-1])+1)
        if len(overlap) > 0:
            print(f"overlap: {compressed_dest}, {current_source}, {overlap}")
        else:
            print(f"no match: {compressed_dest}, {current_source}")

    print("---")
