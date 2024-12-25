import itertools


def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse_key(string):
    key = [list(reversed(string[i::6])) for i in range(5)]
    key_heights = [s.index('.') - 1 for s in key]
    return key_heights

def parse_lock(string):
    lock = [string[i::6] for i in range(5)]
    lock_heights = [s.index('.') - 1 for s in lock]
    return lock_heights

def fits(key, lock):
    return all([k+l < 6 for k, l in zip(key, lock)])

def parse(string):
    key_or_lock_list = string.split("\n\n")
    keys = []
    locks = []
    for key_or_lock in key_or_lock_list:
        if key_or_lock[0] == '#':
            locks.append(parse_lock(key_or_lock))
        if key_or_lock[-1] == '#':
            keys.append(parse_key(key_or_lock))
    return keys, locks

def run(file="input.txt"):
    keys, locks = parse(read(file))
    total_fits = 0
    for lock, key in itertools.product(locks, keys):
        if fits(key, lock):
            total_fits += 1
    return total_fits

if __name__ == "__main__":
    print(run(file="example.txt"))
    print(run())
    # print(run2())
