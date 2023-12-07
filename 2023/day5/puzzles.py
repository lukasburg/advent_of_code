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
        section_map.append(((source_start, source_start + source_range-1), (dest_start, dest_start + source_range-1)))
    sorted_map = sorted(section_map, key=lambda t: t[0][0])
    mappers2.append(sorted_map)


compressed_mapper = mappers2[0]
for current_mapper in mappers2[1:]:
    new_compressed = []
    for compressed_ranges, current_ranges in itertools.product(compressed_mapper, current_mapper):
        compressed_start, compressed_end = compressed_ranges[1]
        current_start, current_end = current_ranges[0]
        print(range(max(compressed_ranges[0], current_ranges[0]), min(compressed_ranges[-1], current_ranges[-1])+1))
        # compressed is completely inside the existing result range
        if current_start <= compressed_start <= current_end and current_start <= compressed_end <= current_end:
            print(f"compressed swallowed: {compressed_ranges}, {current_ranges}")
            # 3 ranges need to be added: possibly before and after, and inside:
        # current is completely inside the existing result range
        elif compressed_start <= current_start <= compressed_end and compressed_start <= current_end <= compressed_end:
            print(f"current swallowed: {compressed_ranges}, {current_ranges}")
            # 3 ranges need to be added: possibly before and after, and inside:
            if compressed_start < current_start:
                amount_before = current_start - compressed_start
                before_source_range = (compressed_ranges[0][0], compressed_ranges[0][0]+amount_before-1)
                before_dest_range = (compressed_ranges[1][0], compressed_ranges[1][0] + amount_before - 1)
                new_compressed.append((before_source_range, before_dest_range))
            if compressed_end > current_end:
                amount_after = compressed_end - current_end
                after_source_range = (compressed_ranges[0][1] - amount_after, compressed_ranges[0][1])
                after_dest_range = (compressed_ranges[1][0], compressed_ranges[1][0] + amount_before - 1)
                new_compressed.append((before_start_range, before_end_range))
        # current start overlaps with compressed end
        elif compressed_start <= current_start <= compressed_end:
            print(f"start of current with end of compressed: {compressed_ranges}, {current_ranges}")
        # current end overlaps with compressed start
        elif compressed_start <= current_end <= compressed_end:
            print(f"end of current with start of compressed: {compressed_ranges}, {current_ranges}")
        else:
            print(f"no match: {compressed_ranges}, {current_ranges}")
    print("---")
