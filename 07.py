from intcode_computer import read_intcode, IntcodeComputer

program = read_intcode(r'inputs\07.txt')

def find_permutations(sequence):
    if len(sequence) <= 1:
        return [sequence]
    else:
        result = []
        char, remainder = sequence[0], sequence[1:]
        for permutation in find_permutations(remainder):
            for i in range(len(permutation) + 1):
                result.append(permutation[:i] + char + permutation[i:])
        return result

def get_output_signal(amps):
    amps[0].extend_inputs([0])
    i = 0
    n = len(amps)
    while not all(amp.finished for amp in amps):
        amps[(i + 1) % n].extend_inputs(amps[i % n].read())
        i += 1
    return amps[0].inputs[-1]

def find_largest_signal(settings, program):
    outputs = []
    for sequence in find_permutations(settings):
        amps = []
        for setting in sequence:
            amps.append(IntcodeComputer(program[:], [int(setting)]))
        outputs.append(get_output_signal(amps))
    return max(outputs)

print('Part 1 answer:', find_largest_signal('01234', program))
print('Part 2 answer:', find_largest_signal('56789', program))
