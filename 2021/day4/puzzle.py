from pprint import pprint


class Board:
    def __init__(self, board):
        self.rows = [set([int(i) for i in row]) for row in board]
        self.cols = [set([int(row[i]) for row in board]) for i in range(len(board))]

    def __str__(self):
        return f"(rows: {self.rows},\n cols: {self.cols})"

    def __repr__(self):
        return str(self)

    def mark(self, number) -> 'Board':
        for line in self.rows+self.cols:
            try:
                line.remove(number)
            except KeyError:
                pass
        return self

    def does_win(self) -> bool:
        for line in self.rows+self.cols:
            if not line:
                return True
        return False

    def score(self, last_number) -> int:
        return sum([number for row in self.rows for number in row])*last_number


with open("input") as file:
    inp = file.readlines()

draws = inp[0]
boards = set([Board([row.strip().split() for row in inp[2+i*6:7+i*6]]) for i in range((len(inp)-1)//6)])


def find_scores(boards):
    no_winner = True
    for number in draws.strip().split(','):
        number = int(number)
        to_remove = set()
        for board in boards:
            board.mark(number)
            if board.does_win():
                to_remove.add(board)
                if no_winner:
                    winner_score = board.score(number)
                    no_winner = False
                if len(boards) <= 1:
                    looser_score = board.score(number)
                    return winner_score, looser_score
        boards = boards.difference(to_remove)
        print(to_remove, len(boards))


print(find_scores(boards))
