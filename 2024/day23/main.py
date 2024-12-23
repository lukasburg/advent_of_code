from collections import defaultdict
from email.policy import default


class PcCluster(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate = False
        for pc in self:
            if pc.startswith('t'):
                self.candidate = True
                break

    def __hash__(self):
        return hash(tuple(sorted(self)))

    def __eq__(self, other):
        return tuple(sorted(self)) == tuple(sorted(other))

    def as_password(self):
        return ','.join(sorted(self))

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    connects_to : dict[str, set] = defaultdict(set)
    connection_pairs = [tuple(p.split("-")) for p in string.split("\n")]
    for a, b in connection_pairs:
        connects_to[a].add(b)
        connects_to[b].add(a)
    return connection_pairs, connects_to

def find_triplets(connection_pairs, connects_to):
    triplets = set()
    for a, b in connection_pairs:
        both_connect_to = connects_to[a].intersection(connects_to[b]).difference({a, b})
        for third_pc in both_connect_to:
            triplets.add(PcCluster({a, b, third_pc}))
    return triplets

def find_bigger_clusters(current_clusters, connects_to):
    bigger_clusters = set()
    for cluster in current_clusters:
        all_connect_to = set.intersection(*(connects_to[pc] for pc in cluster))
        for m_th_pc in all_connect_to:
            bigger_clusters.add(PcCluster(cluster.union({m_th_pc})))
    return bigger_clusters


def is_candidate(triplet):
    return triplet.candidate

def candidate_triplets_part1(connection_pairs, connects_to):
    triplets = find_triplets(connection_pairs, connects_to)
    candidates = list(filter(is_candidate, triplets))
    return len(candidates)

def biggest_cluster_part2(connection_pairs, connects_to):
    # start with pairs
    current_clusters = {PcCluster({a, b}) for a, b in connection_pairs}
    while len(current_clusters) > 1:
        previous_clusters = current_clusters
        current_clusters = find_bigger_clusters(current_clusters, connects_to)
    try:
        return current_clusters.pop()
    except KeyError as e:
        print(previous_clusters)
        raise e

def run(file="input.txt"):
    connection_pairs, connects_to = parse(read(file))
    part1 = candidate_triplets_part1(connection_pairs, connects_to)
    part2 = biggest_cluster_part2(connection_pairs, connects_to).as_password()
    return part1, part2

if __name__ == "__main__":
    print(run(file="example.txt"))
    print(run())
