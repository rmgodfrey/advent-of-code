PARAM_TYPES = {
    1: 'rrw', 2: 'rrw', 3: 'w',
    4: 'r', 5: 'rr', 6: 'rr',
    7: 'rrw', 8: 'rrw', 9: 'r',
    99: '',
}

def read_intcode(file):
    with open(file) as f:
        program = f.read().split(',')
    for i in range(len(program)):
        program[i] = int(program[i])
    return program

class IntcodeComputer:
    '''
    Inputs and outputs are assumed to be lists, so that
    the computer can store multiple inputs (each element of the list),
    and return multiple outputs.
    '''

    def __init__(self, program, input_list):
        self.program = dict(enumerate(program))
        self.inputs = input_list
        self.relative_base = 0
        self.position = 0
        self.finished = False
    
    def get(self, key):
        return self.program.get(key, 0)
    
    def extend_inputs(self, inputs):
        self.inputs.extend(inputs)
    
    def read(self):
        outputs = []
        program = self.program
        while True:
            instruction = str(program[self.position])
            opcode = int(instruction[-2:])
            param_length = len(PARAM_TYPES[opcode])
            modes = instruction[:-2].zfill(param_length)
            parameters = []
            for i in range(1, param_length + 1):
                adjustment = self.relative_base if int(modes[-i]) == 2 else 0
                if int(modes[-i]) == 1:
                    parameters.append(self.position + i)
                else:
                    parameters.append(self.get(self.position + i) + adjustment)
            if opcode == 1:
                program[parameters[2]] = (self.get(parameters[0])
                                          + self.get(parameters[1]))
            elif opcode == 2:
                program[parameters[2]] = (self.get(parameters[0])
                                          * self.get(parameters[1]))
            elif opcode == 3:
                if not self.inputs:
                    return outputs
                program[parameters[0]] = self.inputs.pop(0)
            elif opcode == 4:
                outputs.append(self.get(parameters[0]))
            elif opcode == 5:
                if program[parameters[0]]:
                    self.position = self.get(parameters[1])
                    continue
            elif opcode == 6:
                if not program[parameters[0]]:
                    self.position = self.get(parameters[1])
                    continue
            elif opcode == 7:
                if self.get(parameters[0]) < self.get(parameters[1]):
                    program[parameters[2]] = 1
                else:
                    program[parameters[2]] = 0
            elif opcode == 8:
                if self.get(parameters[0]) == self.get(parameters[1]):
                    program[parameters[2]] = 1
                else:
                    program[parameters[2]] = 0
            elif opcode == 9:
                self.relative_base += self.get(parameters[0])
            elif opcode == 99:
                self.finished = True
                return outputs
            self.position += param_length + 1
