import itertools
import re

from numpy.ma.core import swapaxes


def read(filename):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    initial_values, gates = string.split('\n\n')
    initial_values = initial_values.split('\n')
    known_cables: dict[str, "Cable"] = dict()
    gates = gates.split('\n')
    gates = [LogicGate.from_string(s, known_cables) for s in gates]
    return gates, initial_values, known_cables

class Cable:
    init_val_matcher = re.compile(r'(\w{3}): (\d)')

    def __init__(self, name):
        self.value = None
        self.name = name
        self.is_set = False
        self.input_gate = None
        self.listeners = []
        if name.startswith('x') or name.startswith('y') or name.startswith('z'):
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
    def parse_value(cls, string, known_cables):
        name, val = cls.init_val_matcher.fullmatch(string).groups()
        known_cables[name].set_value(True if int(val) == 1 else False)

    @classmethod
    def get_or_create_cable(cls, name, known_cables):
        if name in known_cables:
            return known_cables[name]
        else:
            cable = Cable(name)
            known_cables[name] = cable
            return cable

class LogicGate:
    symbol = " GENERIC GATE, DO NOT USE "
    gate_matcher = re.compile(r'(\w{3}) (\w{2,3}) (\w{3}) -> (\w{3})')

    def __init__(self, cable_in_1, cable_in_2, cable_out):
        self.cable_in_1 = cable_in_1
        self.cable_in_2 = cable_in_2
        cable_in_1.add_listener(self)
        cable_in_2.add_listener(self)
        self.cable_out = cable_out

    def update(self):
        if self.cable_in_1.is_set & self.cable_in_2.is_set:
            self.cable_out.set_value(self.calculate_output())

    def calculate_output(self):
        raise NotImplemented

    @classmethod
    def from_string(cls, string, known_cables):
        c1, op, c2, c_out = cls.gate_matcher.fullmatch(string).groups()
        c1 = Cable.get_or_create_cable(c1, known_cables)
        c2 = Cable.get_or_create_cable(c2, known_cables)
        c_out = Cable.get_or_create_cable(c_out, known_cables)
        gate = None
        if op == 'AND':
            gate = AndGate(c1, c2, c_out)
        elif op == 'OR':
            gate = OrGate(c1, c2, c_out)
        elif op == 'XOR':
            gate = XorGate(c1, c2, c_out)
        else:
            raise ValueError
        c_out.input_gate = gate
        return gate

    def render_formula(self):
        if self.cable_in_1.input_gate is None:
            gate_1_formula = self.cable_in_1.name
        else:
            gate_1_formula = self.cable_in_1.input_gate.render_formula()
        if self.cable_in_2.input_gate is None:
            gate_2_formula = self.cable_in_2.name
        else:
            gate_2_formula = self.cable_in_2.input_gate.render_formula()
        return f"({gate_1_formula} {self.symbol} {gate_2_formula})"

class AndGate(LogicGate):
    symbol = '∧'
    def calculate_output(self):
        return self.cable_in_1.value & self.cable_in_2.value

class OrGate(LogicGate):
    symbol = '∨'
    def calculate_output(self):
        return self.cable_in_1.value | self.cable_in_2.value

class XorGate(LogicGate):
    symbol = '⊕'
    def calculate_output(self):
        return self.cable_in_1.value ^ self.cable_in_2.value

def cable_list(output_cables):
    return sorted(output_cables, key=lambda c: c.index, reverse=True)

def print_cable_set_value(sorted_cables):
    return int(''.join(map(lambda c: '1' if c.value else '0', sorted_cables)), 2)

def read_start_values(initial_values, known_cables):
    for initial_value in initial_values:
        Cable.parse_value(initial_value, known_cables)

def run(file="input.txt"):
    gates, initial_values, known_cables = parse(read(file))
    output_cables = cable_list(set({c for c in known_cables.values() if c.name.startswith('z')}))
    read_start_values(initial_values, known_cables)
    out = print_cable_set_value(output_cables)
    return out

def alph():
    for p in ['', 'a', 'b', 'c']:
        for i in range(97, 121):
            if chr(i) == "x" or chr(i) == "y":
                continue
            yield p + chr(i)

def run2(file="input.txt"):
    gates, initial_values, known_cables = parse(read(file))
    x_cables = cable_list(set({c for c in known_cables.values() if c.name.startswith('x')}))
    y_cables = cable_list(set({c for c in known_cables.values() if c.name.startswith('y')}))
    z_cables = cable_list(set({c for c in known_cables.values() if c.name.startswith('z')}))
    read_start_values(initial_values, known_cables)
    current_z = print_cable_set_value(z_cables)
    y = print_cable_set_value(y_cables)
    x = print_cable_set_value(x_cables)
    sum_x_y = x + y
    missmatch = sum_x_y ^ current_z
    print(f"x+y:  {sum_x_y:050b}")
    print(f"z:    {current_z:050b}")
    print(f"miss: {missmatch:050b}")
    wrong_indices = map(lambda t: t[0], filter(
        lambda t: t[1], zip(range(50), map(lambda b: True if b == '1' else False, list(bin(missmatch))[:2:-1]))))
    for j in range(len(x_cables), 0, -1):
        print(z_cables[j].name, z_cables[j].input_gate.render_formula())
        f = z_cables[j].input_gate.render_formula()
        alphabet = alph()
        for j in range(len(x_cables)):
            if f'{j:02}' in f:
                s = next(alphabet)
                f = f.replace(f'x{j:02}', s)
                f = f.replace(f'y{j:02}', s.upper())
        print(f)

if __name__ == "__main__":
    print(run(file="example.txt"))
    print(run(file="example2.txt"))
    print(run())
    print(run2())
