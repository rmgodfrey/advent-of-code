from intcode_computer import read_intcode, IntcodeComputer

program = read_intcode(r'inputs\09.txt')

print('Part 1 answer:', IntcodeComputer(program, [1]).read()[-1])
print('Part 2 answer:', IntcodeComputer(program, [2]).read()[-1])
