from intcode_computer import read_intcode

def run_intcode(intcode, noun, verb):
    intcode[1] = noun
    intcode[2] = verb
    i = 0
    while True:
        opcode = intcode[i]
        if opcode == 99:
            break
        position1 = intcode[i+1]
        position2 = intcode[i+2]
        output_position = intcode[i+3]
        if opcode == 1:
            intcode[output_position] = intcode[position1] + intcode[position2]
            step = 4
        if opcode == 2:
            intcode[output_position] = intcode[position1] * intcode[position2]
            step = 4
        i += step
    return intcode[0]


def find_input_pairs(program, desired_output):
    i = 0
    while i < 100:
        if run_intcode(program[:], i, i) == desired_output:
            return (i, i)
        for j in range(i):
            if run_intcode(program[:], i, j) == desired_output:
                return (i, j)
            if run_intcode(program[:], j, i) == desired_output:
                return (j, i)
        i += 1                

program = read_intcode(r'inputs\02.txt')

print('Part 1 answer:', run_intcode(program[:], 12, 2))

DESIRED_OUTPUT = 19690720
noun, verb = find_input_pairs(program, DESIRED_OUTPUT)

print('Part 2 answer:', 100*noun + verb)
