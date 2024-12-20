def read(filename="input.txt"):
    with open(filename) as file:
        return file.read()[:-1]

def parse(string):
    memory, instructions = string.split("\n\n")
    ins = [int(i) for i in instructions[9:].split(",")]
    return ins

opcode_to_verb = [
    "adv",
    "bxl",
    "bst",
    "jnz",
    "bxc",
    "out",
    "bdv",
    "cdv",
]

opcode_to_higher_level_language = {
    'adv': lambda operand: f"A = A // (2^{operand})",
    'bxl': lambda operand: f"B = B XOR {operand}",
    'bst': lambda operand: f"B = {operand} % 8",
    'jnz': lambda operand: f"}} while (A != 0)",
    'bxc': lambda operand: f"B = B XOR C",
    'out': lambda operand: f"print {operand} % 8",
    'bdv': lambda operand: f"B = A // (2^{operand})",
    'cdv': lambda operand: f"C = A // (2^{operand})",
}

opcode_combo = {
    'adv': True,
    'bxl': False,
    'bst': True,
    'jnz': False,
    'bxc': False,
    'out': True,
    'bdv': True,
    'cdv': True,
}

def combo_operand_decompile(operand):
    if operand in range(4):
        return operand
    if operand == 4:
        return 'A'
    if operand == 5:
        return 'B'
    if operand == 6:
        return 'C'
    raise RuntimeError

def decompile_opcode_operand(code, operand):
    if opcode_combo[code]:
        return combo_operand_decompile(operand)
    else:
        return operand

def number_to_opcode(number):
    return opcode_to_verb[number]

def decompile_line_to_verb(number, operand):
    verb = number_to_opcode(number)
    return verb, decompile_opcode_operand(verb, operand)

def decompile_line_to_higher_level_language(number, operand):
    verb = number_to_opcode(number)
    return opcode_to_higher_level_language[verb](decompile_opcode_operand(verb, operand))

def decompile_program(program, level):
    opcode_operand_list = zip(program[::2], program[1::2])
    decompiled_program = []
    for code, operand in opcode_operand_list:
        if level == 0:
            decompiled_program.append(decompile_line_to_verb(code, operand))
        elif level == 1:
            line = decompile_line_to_higher_level_language(code, operand)
            if opcode_to_verb[code] == 'jnz':
                decompiled_program[operand // 2] = 'do { ' + decompiled_program[operand // 2]
            decompiled_program.append(line)
    return decompiled_program

def render(original_program, decompiled_program, show_original_instructions=False):
    if show_original_instructions:
        return '\n'.join(map(lambda i: f"{i[1]} {' ' * (40 - len(i[1]))}# {i[0]}", zip(original_program, decompiled_program)))
    return '\n'.join(decompiled_program)

def run(file="input.txt"):
    program = parse(read(file))
    o_p = zip(program[::2], program[1::2])
    d = decompile_program(program, 1)
    with open('decompiled.txt', 'w') as file:
        file.write(render(o_p, d))

if __name__ == "__main__":
    run()
