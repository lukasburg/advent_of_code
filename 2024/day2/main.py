def get_input(filename="input"):
    with open(filename) as file:
        return file.read()


def parse_input(string):
    return [[int(v) for v in line.split(" ")] for line in string.split("\n")[:-1]]


def check_line_recursively(line, ascending=None):
    if len(line) < 2:
        return True
    if 0 < line[0] - line[1] < 4 and (ascending or ascending is None):
        return check_line_recursively(line[1:], True)
    if -4 < line[0] - line[1] < 0 and (not ascending or ascending is None):
        return check_line_recursively(line[1:], False)
    else:
        return False


def check_line_recursively_with_removing(line, ascending=None, skipped_once = False, previous_number=None):
    if len(line) < 2:
        return True
    if 0 < line[0] - line[1] < 4 and (ascending or ascending is None):
        if check_line_recursively_with_removing(line[1:], True, skipped_once, line[0]):
            return True
    if -4 < line[0] - line[1] < 0 and (not ascending or ascending is None):
        if check_line_recursively_with_removing(line[1:], False, skipped_once, line[0]):
            return True
    if not skipped_once:
        if len(line) >= 3:
            if 0 < line[0] - line[2] < 4 and (ascending or ascending is None):
                if check_line_recursively_with_removing(line[2:], True, True, line[0]):
                    return True
            if -4 < line[0] - line[2] < 0 and (not ascending or ascending is None):
                if check_line_recursively_with_removing(line[2:], False, True, line[0]):
                    return True
        # if only one number remaining, just skip and all is fine
        else:
            return True
        if previous_number:
            return check_line_recursively_with_removing([previous_number] + line[1:], ascending, True)
        else:
            return check_line_recursively_with_removing(line[1:], ascending, True)
    return False


def run():
    # part one
    lines = parse_input(get_input())
    for line in lines:
        # print(check_line_recursively(line), line)
        pass
    # part two
    total_with_dampener = 0
    for line in lines:
        print(check_line_recursively_with_removing(line), line)
        if check_line_recursively_with_removing(line):
            total_with_dampener += 1
    print(total_with_dampener)


if __name__ == "__main__":
    run()
