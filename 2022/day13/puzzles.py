from itertools import zip_longest

with open('input') as file:
    inp = file.read()


class WrongOrderException(Exception):
    pass


class MessageList(list):
    def __lt__(self, other):
        try:
            return compare(self, other)
        except WrongOrderException:
            return False


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if right < left:
            raise WrongOrderException
        if left < right:
            return True
        return False
    elif isinstance(left, list) and isinstance(right, list):
        for l_el, r_el in zip_longest(left, right):
            if l_el is None and r_el is None:
                return False
            if l_el is None:
                return True
            if r_el is None:
                raise WrongOrderException
            if compare(l_el, r_el):
                return True
    else:  # one list, one integer
        left = [left] if not isinstance(left, list) else left
        right = [right] if not isinstance(right, list) else right
        if compare(left, right):
            return True


def run():
    right_indizes = []
    wrong_order = []
    for index, pair in enumerate(inp.strip().split('\n\n')):
        strings = pair.split('\n')
        left, right = eval(strings[0]), eval(strings[1])
        try:
            if compare(left, right):
                right_indizes.append(index+1)
            else:
                raise RuntimeError(f'No decision for {index+1}')
        except WrongOrderException:
            wrong_order.append((left, right))
            pass
    print('\nPairs in right order: ', right_indizes, ',\n sum: ', sum(right_indizes))
    print('\n\n\n===\n\n\n')


run()


def order():
    key2, key6 = MessageList([[2]]), MessageList([[6]])
    lists = [key2, key6]
    for lst in inp.split('\n'):
        if not lst:
            continue
        parsed = eval(lst.strip())
        lists.append(MessageList(parsed))
    ordered = sorted(lists)
    decoder_key = (ordered.index(key2)+1) * (ordered.index(key6)+1)
    print('Ordered: ', ordered, '\n decoder key: ', decoder_key)


order()
