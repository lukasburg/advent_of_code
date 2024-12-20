import re
from datetime import datetime
from multiprocessing import Pool

from numpy.testing.print_coercion_tables import print_coercion_table


class Memory:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"(A:{self.a:b} B:{self.b:b} C:{self.c:b})"

def read(filename="input.txt"):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    memory, instructions = string.split("\n\n")
    start_values = re.findall(r"(\d+)", memory)
    mem = Memory(*[int(v) for v in start_values])
    ins = [int(i) for i in instructions[9:].split(",")]
    return mem, ins

def combo_value(operand, mem):
    if operand in {0, 1, 2, 3}:
        return operand
    if operand == 4:
        return mem.a
    if operand == 5:
        return mem.b
    if operand == 6:
        return mem.c
    raise ValueError(f"Invalid operand {operand}")

def division(operand, mem):
    numerator = mem.a
    denominator = pow(2, combo_value(operand, mem))
    return int(numerator / denominator)

def adv(operand, mem):
    mem.a = division(operand, mem)

def bxl(operand, mem):
    mem.b = mem.b ^ operand

def bst(operand, mem):
    mem.b = combo_value(operand, mem) % 8

def jnz(operand, mem, pointer):
    if mem.a == 0:
        return pointer
    return operand - 2

def bxc(_, mem):
    mem.b = mem.b ^ mem.c

def out(operand, mem, terminal_out):
    terminal_out.append(combo_value(operand, mem) % 8)

def bdv(operand, mem):
    mem.b = division(operand, mem)

def cdv(operand, mem):
    mem.c = division(operand, mem)

opcode_to_fun = [
    adv,
    bxl,
    bst,
    jnz,
    bxc,
    out,
    bdv,
    cdv
]

def interpret(memory, ins):
    instruction_pointer = 0
    terminal_out = []
    while instruction_pointer < len(ins):
        opcode, operand = ins[instruction_pointer], ins[instruction_pointer + 1]
        fun = opcode_to_fun[opcode]
        if fun == jnz:
            instruction_pointer = fun(operand, memory, instruction_pointer)
        elif fun == out:
            fun(operand, memory, terminal_out)
        else:
            fun(operand, memory)
        instruction_pointer += 2
    return terminal_out

def match(target, until_now):
    return until_now == target[:len(until_now)]

def match_end(target, until_now):
    return until_now == target[len(target) - len(until_now):]

def interpret_until_false(memory, ins, target_terminal):
    instruction_pointer = 0
    terminal_out = []
    while instruction_pointer < len(ins):
        opcode, operand = ins[instruction_pointer], ins[instruction_pointer + 1]
        fun = opcode_to_fun[opcode]
        if fun == jnz:
            instruction_pointer = fun(operand, memory, instruction_pointer)
        elif fun == out:
            fun(operand, memory, terminal_out)
        else:
            fun(operand, memory)
        instruction_pointer += 2
        if not match(target_terminal, terminal_out):
            return terminal_out
    return terminal_out

def run(file="input.txt"):
    mem, ins = parse(read(file))
    terminal_out = interpret(mem, ins)
    print(",".join(map(str, terminal_out)))

def try_i(i, original_mem, ins):
    mem = Memory(i, original_mem.b, original_mem.c)
    if i % 1000000 == 0:
        terminal_out = interpret(mem, ins)
        # print(i, len(terminal_out), datetime.now())
        # print(f'{terminal_out}')
    else:
        terminal_out = interpret(mem, ins)
    if terminal_out == ins:
        print(f'A {i} is a solution')
        return terminal_out
    return terminal_out


def run2(original_mem, ins):
    i_start = pow(8, len(ins) - 1) - (pow(8, len(ins) - 10))
    i_end = pow(8, len(ins))
    for i in range(i_start, i_end):
        try_i(i, original_mem, ins)
    # print(res)
    raise RuntimeError(f'No solution found, tried from {i_start} until {i_end}')

def reassemble_target(ins, original_mem):
    mem_a = 0
    for j in range(len(ins)):
        for i in range(1000000):   # don't know why this works
            target_n = try_i(mem_a + i, original_mem, ins)
            if match_end(ins, target_n):
                mem_a += i
                print(mem_a)
                print(target_n)
                break
        else:
            print(f'No solution found for {j}: {target_n}')
        mem_a *= 8  # shift left 3 positions
    return mem_a

if __name__ == "__main__":
    orig_mem, instructions = parse(read("input.txt"))
    target_a_from_reverse_engineering = reassemble_target(instructions, orig_mem)
    print(target_a_from_reverse_engineering)
    # print(try_i(target_a_from_reverse_engineering, orig_mem, instructions))
    # run2(orig_mem, instructions)
