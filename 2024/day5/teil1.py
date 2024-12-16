def get_input(filename='input'):
    with open(filename) as file:
        string = file.read()
        return string


def parse_input(string):
    o_r_string, m_string = string.split('\n\n')
    o_r = o_r_string.split('\n')
    m = m_string.split('\n')[:-1]
    return [(int(a) for a in t.split("|")) for t in o_r], [[int(a) for a in n.split(",")] for n in m]



def is_correct_manual(manual):
    pages_not_allowed_anymore = set()
    for page in manual:
        if page in pages_not_allowed_anymore:
            return False
        pages_not_allowed_anymore = pages_not_allowed_anymore.union(forbidden_after[page])
    return True



ordering_rules, manuals = parse_input(get_input())
forbidden_after = {
    i: set() for i in range(100)
}
must_come_before = {
    i: set() for i in range(100)
}
for before, after in ordering_rules:
    forbidden_after[after].add(before)
    must_come_before[before].add(after)


def sort_manual(manual):
    sorted_manual = []
    for page in manual:
        pages_before = must_come_before[page]
        index_list = []
        for pb in pages_before:
            try:
                index_list.append(sorted_manual.index(pb))
            except ValueError:
                pass
        index_list.append(len(sorted_manual))
        sorted_manual.insert(min(index_list), page)
    return sorted_manual


total_correct = 0
total_sorted = 0
for manual in manuals:
    if is_correct_manual(manual):
        middle_page = manual[len(manual)//2]
        total_correct += middle_page
    else:
        s_m = sort_manual(manual)
        middle_page = s_m[len(s_m)//2]
        total_sorted += middle_page


print(total_correct)
print(total_sorted)
