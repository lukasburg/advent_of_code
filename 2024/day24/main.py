import re

def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    initial_values, gates = string.split('\n\n')
    initial_values = initial_values.split('\n')
    gates = gates.split('\n')
    gates = [LogicGate.from_string(s) for s in gates]
    return gates, initial_values


known_cables : dict[str, "Cable"] = dict()
output_cables = set()

class Cable:
    init_val_matcher = re.compile(r'(\w{3}): (\d)')

    def __init__(self, name):
        self.value = None
        self.name = name
        self.is_set = False
        self.listeners = []
        if name.startswith('z'):
            output_cables.add(self)
            self.index = int(name[1:])

    def set_value(self, value):
        self.value = value
        self.is_set = True
        for listener in self.listeners:
            listener.update()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def __repr__(self):
        return f'Cable({self.name}: {self.value})'

    @classmethod
    def parse_value(cls, string):
        name, val = cls.init_val_matcher.fullmatch(string).groups()
        known_cables[name].set_value(True if int(val) == 1 else False)

    @classmethod
    def get_or_create_cable(cls, name):
        if name in known_cables:
            return known_cables[name]
        else:
            cable = Cable(name)
            known_cables[name] = cable
            return cable

class LogicGate:
    gate_matcher = re.compile(r'(\w{3}) (\w{2,3}) (\w{3}) -> (\w{3})')

    def __init__(self, cable_in_1, cable_in_2, cable_out):
        self.cables_in = cable_in_1, cable_in_2
        cable_in_1.add_listener(self)
        cable_in_2.add_listener(self)
        self.cable_out = cable_out

    def update(self):
        if self.cables_in[0].is_set & self.cables_in[1].is_set:
            self.cable_out.set_value(self.calculate_output())

    def calculate_output(self):
        raise NotImplemented

    @classmethod
    def from_string(cls, string):
        c1, op, c2, c_out = cls.gate_matcher.fullmatch(string).groups()
        c1 = Cable.get_or_create_cable(c1)
        c2 = Cable.get_or_create_cable(c2)
        c_out = Cable.get_or_create_cable(c_out)
        if op == 'AND':
            return AndGate(c1, c2, c_out)
        if op == 'OR':
            return OrGate(c1, c2, c_out)
        if op == 'XOR':
            return XorGate(c1, c2, c_out)
        raise ValueError


class AndGate(LogicGate):
    def calculate_output(self):
        return self.cables_in[0].value & self.cables_in[1].value

class OrGate(LogicGate):
    def calculate_output(self):
        return self.cables_in[0].value | self.cables_in[1].value

class XorGate(LogicGate):
    def calculate_output(self):
        return self.cables_in[0].value ^ self.cables_in[1].value

def output():
    sorted_cables = sorted(output_cables, key=lambda c: c.index, reverse=True)
    return ''.join(map(lambda c: '1' if c.value else '0', sorted_cables))


def run(file="input.txt"):
    gates, initial_values = parse(read(file))
    for initial_value in initial_values:
        Cable.parse_value(initial_value)
    out = output()
    return out, int(out, 2)


if __name__ == "__main__":
    print(run(file="example.txt"))
    print(run(file="example2.txt"))
    print(run())
    # print(run2(file="example2.txt"))
    # print(run2())
