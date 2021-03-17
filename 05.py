from intcode_computer import IntcodeComputer, read_intcode

program = read_intcode(r'inputs\05.txt')

print('Part 1 answer:', IntcodeComputer(program[:], [1]).read()[-1])
print('Part 2 answer:', IntcodeComputer(program[:], [5]).read()[-1])