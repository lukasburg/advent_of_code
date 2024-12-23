from collections import defaultdict
from itertools import product
import progressbar


def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    start_secrets = string.split("\n")
    return list(map(int, start_secrets))

def mix(secret, given_number):
    return secret ^ given_number

def prune(secret):
    return secret & (16777216 - 1)   # c % 16777216

def next_secret(current_secret):
    current_secret = (current_secret ^ (current_secret << 6)) & (16777216 - 1)  # prune(mix(c, c * 64))
    current_secret = (current_secret ^ (current_secret >> 5)) & (16777216 - 1)  # prune(mix(c, c // 32))
    current_secret = (current_secret ^ (current_secret << 11)) & (16777216 - 1) # prune(mix(c, c * 2048))
    return current_secret

def all2000secret(start, i=2001):
    c = start
    for _ in range(i):
        yield c
        c = next_secret(c)

def create_last_digits(start_secret):
    return [c % 10 for c in all2000secret(start_secret)]

def create_differences(last_digits):
    return [c2 - c1 for c1, c2 in zip(last_digits, last_digits[1:])]

def hash_sequence(*values):
    values = [v+9 for v in values]
    return sum([v*(20**i) for i, v in enumerate(values)])

def price_at_sequence(secret):
    prices = create_last_digits(secret)
    differences = create_differences(prices)
    sequence_to_price = defaultdict(lambda: 0)
    for price, *sequence in zip(prices[4:], differences, differences[1:], differences[2:], differences[3:]):
        hash_val = hash_sequence(*sequence)
        if hash_val not in sequence_to_price:
            sequence_to_price[hash_val] = price
    return sequence_to_price

def last_of_iter(iterator):
    for i in iterator:
        continue
    return i

def valid_sequences_iterator():
    def mini_diffs(l):
        return [c1 - c2 for c1, c2 in zip(l, l[1:])]
    for vals in [mini_diffs(p) for p in product(range(10), repeat=5)]:
        yield vals

def score_of_sequence(hashed_sequence, prices):
    return sum([p[hashed_sequence] for p in prices])

def run(file="input.txt"):
    secrets = parse(read(file))
    # o_s = secrets
    secrets = [last_of_iter(all2000secret(s)) for s in secrets]
    # for start, secret in zip(o_s, secrets):
    #     print(f"{start}: {secret}")
    return sum(secrets)

def run2(file="input.txt"):
    secrets = parse(read(file))
    o_s = secrets
    prices_at_seqs = [price_at_sequence(s) for s in secrets]
    max_score = 0
    best_sequence = None
    with progressbar.ProgressBar(max_value=progressbar.UnknownLength) as bar:
        for sequence in valid_sequences_iterator():
            score = score_of_sequence(hash_sequence(*sequence), prices_at_seqs)
            bar.next()
            if score > max_score:
                max_score = score
                # print(max_score, sequence)
                best_sequence = sequence
    return max_score
    # for start, prices in zip(o_s, prices_at_seqs):
    #     print(f"{start}: {prices[hash_sequence(-2,1,-1,3)]}")

if __name__ == "__main__":
    print(run(file="example.txt"))
    print(run())
    print(run2(file="example2.txt"))
    print(run2())

# -1,1,-1,2