class Hull:
    def __init__(self, painter, start_color):
        '''
        Each hull stores a dictionary of panels in the hull.
        Each key is a coordinate representing the location of the panel;
        Each value is the panel itself. At initialization, a single panel
        is stored at the origin.
        '''
        self.panels = {(0, 0): Panel(start_color)}
        self.painter = painter
    
    def __iter__(self):
        for panel in self.panels:
            yield panel
    
    def __getitem__(self, key):
        return self.panels[key]
    
    def __len__(self):
        return len(self.panels)
    
    def expand(self, coord):
        '''
        If panel at coord is already in self.panels, this does
        nothing. If not, it adds a black panel to self.panels
        at the given coord.
        '''
        self.panels.setdefault(coord, Panel(0))
    
    def __str__(self):
        x_coords, y_coords = ([coord[i] for coord in self]
                              for i in range(2))
        
        x_coords.sort(); y_coords.sort()
        
        x_max, x_min = x_coords[-1], x_coords[0]
        y_max, y_min = y_coords[-1], y_coords[0]
        
        rows = []
        yrange = range(y_max + 1, y_min - 2, -1)
        xrange = range(x_min - 1, x_max + 2)
        for y in yrange:
            rows.append([])
            for x in xrange:
                if self.painter.position == (x, y):
                    rows[-1].append(str(self.painter))
                else:
                    rows[-1].append(str(self.panels.get((x, y), '.')))
            rows[-1] = ''.join(rows[-1])
        return '\n'.join(rows)    

class Panel:
    def __init__(self, color):
        '''
        Each panel has a color: 0 represents black, 1 represents white.
        '''
        self.color = color
    
    def __str__(self):
        return '#' if self.color else '.'

class Painter:
    
    # `FORWARD` describes what counts as a forward step for each of
    # the four directions UP, RIGHT, DOWN, LEFT (in that order).
    # (For example, (0, 1) means x-coordinate stays the same,
    # y-coordinate increases by one.)
    FORWARD = ((0, 1), (1, 0), (0, -1), (-1, 0))
    
    def __init__(self):
        '''
        Direction code: 0 for up, 1 for right, 2 for down, 3 for left.
        '''
        self.dir = 0
        self.position = (0, 0)
        self.activated = False # Set to True if at least one panel
                               # has been painted.
    
    def read(self, hull):
        '''
        Reads the color of the panel of the painter's current
        position.
        '''
        return hull[self.position].color
    
    def paint(self, hull, code):
        hull[self.position].color = code
    
    def turn(self, code):
        code = code if code else -1   # 1 stays 1, 0 becomes -1
        self.dir = (self.dir + code) % 4
    
    def step_forward(self):
        step = self.FORWARD[self.dir]
        self.position = tuple(
            self.position[i] + step[i] for i in range(len(self.position))
        )
    
    def activate(self, hull, intcode):
        while not intcode.finished:
            self.activated = True
            hull.expand(self.position)
            intcode.extend_inputs([self.read(hull)])
            color_code, turn_code = intcode.read()
            self.paint(hull, color_code)
            self.turn(turn_code)
            self.step_forward()
    
    def __str__(self):
        return ('^', '>', 'v', '<')[self.dir]

def main(program, start_color=0):
    intcode = IntcodeComputer(program, [])
    hull = Hull(Painter(), start_color)
    hull.painter.activate(hull, intcode)
    return hull

if __name__ == '__main__':
    from intcode_computer import read_intcode, IntcodeComputer
    program = read_intcode(r'inputs\11.txt')
    
    print('Part 1 answer:')
    hull = main(program)
    print(0 if not hull.painter.activated else len(hull))
    
    print()
    
    print('Part 2 answer:')
    hull = main(program, start_color=1)
    print(hull)
