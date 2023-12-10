from pprint import pprint
from typing import Optional

with open("input") as file:
    inp = file.read()


sections = inp[:-1].split("\n\n")
seeed_nums = [int(i) for i in sections[0].split(":")[1].split()]
seeeds = [
    range(seeed_nums[i], seeed_nums[i]+seeed_nums[i+1])
    for i in range(0, len(seeed_nums), 2)
]
min_seeed = min(map(lambda k: k.start, seeeds))
max_seeed = max(map(lambda k: k.stop, seeeds))
print(f"Seed min: {min_seeed}, max: {max_seeed}, {seeeds}")


class FunctionInterval:
    def __init__(self, start_source, range_, start_dest=None, shift=None):
        self.start = start_source
        self.stop = start_source + range_
        self.shift = shift if shift is not None else start_dest - start_source

    def start_range(self):
        return range(self.start, self.stop)

    def end_range(self):
        return range(self.start + self.shift, self.stop + self.shift)

    def __str__(self):
        return f"{self.start_range()} -> {self.end_range()}"

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.start_range())


def range_overlap(range1: range, range2: range) -> range:
    overlap = range(max(range1[0], range2[0]), min(range1[-1], range2[-1]) + 1)
    return overlap if len(overlap) > 0 else None


def compress_second_interval_into_first_if_overlap(
        interval1: FunctionInterval,
        interval2: FunctionInterval
) -> tuple[Optional[FunctionInterval], Optional[FunctionInterval], Optional[FunctionInterval]]:
    overlap = range_overlap(interval1.end_range(), interval2.start_range())
    if overlap:
        part_before = range(interval1.end_range().start, interval2.start)
        part_after = range(interval2.stop, interval1.end_range().stop)
        interval_before = FunctionInterval(interval1.start, len(part_before), start_dest=interval1.end_range().start)
        interval_after = FunctionInterval(part_after.start - interval1.shift, len(part_after), start_dest=part_after.start)
        interval_overlap = FunctionInterval(interval1.start + len(part_before), len(overlap), shift=interval1.shift+interval2.shift)
        return (interval_before if len(interval_before) > 0 else None,
                interval_overlap,
                interval_after if len(interval_after) > 0 else None)
    else:
        return (interval1, None, None)


functions: list[set] = [{FunctionInterval(min_seeed, max_seeed-min_seeed, shift=0)}]
# functions: list[set] = [{FunctionInterval(0, 100, shift=0)}]
for section in sections[1:]:
    # section map is dict like this:    {[source_start, source_end]: shift_by_this_value}
    section_intervals = set()
    lines = section.split("\n")
    for line in lines[1:]:
        dest_start, source_start, source_range = [int(num) for num in line.split()]
        section_intervals.add(FunctionInterval(source_start, source_range, dest_start))
    functions.append(section_intervals)


# pprint(functions)
# pprint(compress_second_interval_into_first_if_overlap(functions[0].pop(), FunctionInterval(50, 48, 52)))

compressed_intervals = functions[0]
for i, function in enumerate(functions[1:]):
    add_later_to_avoid_overlap = set()
    for new_interval in function:
        new_compressed = set()
        for interval_in_compressed in compressed_intervals:
            before, new, after = compress_second_interval_into_first_if_overlap(interval_in_compressed, new_interval)
            new_compressed = new_compressed.union({before, after}.difference({None}))
            add_later_to_avoid_overlap.add(new)
        compressed_intervals = new_compressed
    compressed_intervals = compressed_intervals.union(add_later_to_avoid_overlap).difference({None})

pprint(sorted(compressed_intervals, key=lambda k: k.end_range().start))


def find_lowest():
    for location_range in sorted(compressed_intervals, key=lambda k: k.end_range().start):
        for seeed_range in seeeds:
            overlap = range_overlap(seeed_range, location_range.start_range())
            if overlap:
                print(overlap.start, overlap.index(overlap.start))
                print(location_range.end_range()[overlap.index(overlap.start)])
                return location_range.end_range()[overlap.index(overlap.start)]


find_lowest()
