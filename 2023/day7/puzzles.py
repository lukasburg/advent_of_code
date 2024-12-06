import random
from collections import defaultdict
from pprint import pprint

CARD_SCORES = list(reversed(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']))
CARD_SCORES_WITH_JOKERS = list(reversed(['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']))
#            five, four,   full h, three,     two pair,  one pair,     high card
HAND_TYPES = list(reversed([[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]))

with open("input") as file:
    inp = file.readlines()


class Hand:
    score_base = len(CARD_SCORES)

    def __init__(self, symbols, bid, jokers=False):
        self.symbols = symbols
        if jokers:
            self.type_score = self._type_score_with_jokers()
            self.tie_breaker_scores = self._card_scores_with_jokers()
        else:
            self.type_score = self._type_score()
            self.tie_breaker_scores = self._card_scores()
        self.score = self._total_score()
        self.bid = int(bid)

    def __str__(self):
        return f"Hand(symbols={self.symbols}, bid={self.bid}, score={self.score})"

    def __repr__(self):
        return str(self)

    def _type_score(self):
        count_cards = defaultdict(lambda: 0)
        for symbol in self.symbols:
            count_cards[symbol] += 1
        repetitions = sorted(count_cards.values(), reverse=True)
        return HAND_TYPES.index(repetitions)

    def _card_scores(self):
        card_scores = []
        for symbol in self.symbols:
            card_scores.append(CARD_SCORES.index(symbol))
        return card_scores

    def _type_score_with_jokers(self):
        count_cards = defaultdict(lambda: 0)
        for symbol in self.symbols:
            count_cards[symbol] += 1
        jokers = count_cards['J']
        del count_cards['J']
        repetitions = sorted(count_cards.values(), reverse=True)
        # only jokers
        if len(repetitions) == 0:
            repetitions = [5]
        else:
            repetitions[0] += jokers
        return HAND_TYPES.index(repetitions)

    def _card_scores_with_jokers(self):
        card_scores = []
        for symbol in self.symbols:
            card_scores.append(CARD_SCORES_WITH_JOKERS.index(symbol))
        return card_scores

    def _total_score(self):
        total_score = 0
        for i in range(5):
            shift = pow(self.score_base, i)
            total_score += (self.tie_breaker_scores[-1 - i] * shift)
        type_shift = pow(self.score_base, 5)
        total_score += self.type_score * type_shift
        return total_score


def quicksort(items: set[Hand]):
    if len(items) <= 1:
        return list(items)
    pivot = random.sample(list(items), 1)[0]
    items.remove(pivot)
    right = {pivot}
    left = set()
    for item in items:
        if item.score <= pivot.score:
            right.add(item)
        else:
            left.add(item)
    return quicksort(right) + quicksort(left)


hands = set()
joker_hands = set()
for line in inp:
    hand = Hand(*line.split())
    hands.add(hand)
    joker_hand = Hand(*line.split(), jokers=True)
    joker_hands.add(joker_hand)


total_winnings = 0
for index, hand in enumerate(quicksort(hands), start=1):
    winning = index * hand.bid
    total_winnings += winning


total_winnings2 = 0
for index, hand in enumerate(quicksort(joker_hands), start=1):
    winning = index * hand.bid
    total_winnings2 += winning


print(f"Total winnings: {total_winnings}")
print(f"Total winnings with jokers: {total_winnings2}")
