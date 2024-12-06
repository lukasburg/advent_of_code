from pprint import pprint

with open("input") as file:
    inp = file.read()


def hash_sequence(sequence):
    return sum([ord(symbol)*pow(17, i) for i, symbol in enumerate(reversed(sequence), start=1)]) % 256


print('---')
print(sum(map(hash_sequence, inp[:-1].split(','))))


class Lens:
    def __init__(self, label, focal):
        self.label = label
        self.focal = focal

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label

    def __str__(self):
        return f"L(l={self.label}, f={self.focal})"

    def __repr__(self):
        return str(self)


boxes = [[] for _ in range(256)]
for step in inp[:-1].split(','):
    if '=' in step:
        l, f = step.split('=')
        f = int(f)
        lens = Lens(l, f)
        box = boxes[hash_sequence(l)]
        if lens in box:
            replace_lens_num = box.index(lens)
            box[replace_lens_num] = lens
        else:
            box.append(lens)
    else:
        l = step[:-1]
        box = boxes[hash_sequence(l)]
        lens = Lens(l, None)
        if lens in box:
            box.remove(lens)

# pprint(boxes)
total_power = 0
for b_index, box in enumerate(boxes, start=1):
    for l_index, lens in enumerate(box, start=1):
        total_power += b_index*l_index*lens.focal

print(total_power)
