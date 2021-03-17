class Wire:
    def __init__(self):
        self.path = []
        self.last_coord = [0, 0]
        self.steps = [0]
    def extend_path(self, cmd):
        new_seg = Segment(self.last_coord, cmd)
        self.path.append(new_seg)
        self.last_coord = new_seg.q
        self.steps.append(self.steps[-1] + new_seg.length())

class Segment:
    def __init__(self, last, cmd):
        self.orientation = cmd[0]
        magnitude = int(cmd[1:])
        self.axis = 0 if self.is_horizontal() else 1
        self.p = last
        self.q = self.p[:]
        self.q[self.axis] += self.multiplier() * magnitude
        self.ends = self.p, self.q
    def is_horizontal(self):
        if self.orientation in ('L', 'R'):
            return True
        return False
    def multiplier(self):
        if self.orientation in ('U', 'R'):
            return 1
        return -1
    def length(self):
        return abs(self.p[self.axis] - self.q[self.axis])
    def __repr__(self):
        return str(self.ends)

origin = [0, 0]

def manhattan_distance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def find_intersections_perpendicular(horizontal, vertical, steps):
    hor_y = horizontal.p[1]  # or horizontal.q[1]
    vert_x = vertical.p[0]  # or vertical.q[0]
    hor_left, hor_right = sorted([horizontal.p[0], horizontal.q[0]])
    vert_bottom, vert_top = sorted([vertical.p[1], vertical.q[1]])
    if (hor_left <= vert_x <= hor_right
        and vert_bottom <= hor_y <= vert_top):
        # If endpoints of the previous segments in the paths
        # intersected, don't count them again.
        if not (horizontal.p[0] == vert_x 
                or hor_y == vertical.p[1]):
            coord = vert_x, hor_y
            return [(coord, manhattan_distance(origin, coord),
                     steps + abs(hor_y - vertical.p[1])  
                           + abs(vert_x - horizontal.p[0]))]
    return []

def find_intersections_coincident(seg1, seg2, steps, axis):
    points = []
    for seg in seg1, seg2:
        points.extend(sorted(end[axis] for end in seg.ends))
    seg1_low, seg1_high, seg2_low, seg2_high = points    
    overlapping_points = []
    for num in range(max(seg1_low, seg2_low),
                     min(seg1_high, seg2_high) + 1):
        if num != seg1.p[axis]:
            coord = num, seg1.p[1 - axis]
            overlapping_points.append((
                coord, manhattan_distance(origin, coord),
                steps + abs(num - seg1.p[axis]) + abs(num - seg2.p[axis])
            ))
    return overlapping_points

def find_intersections(seg1, seg2, steps):
    if seg1.is_horizontal() != seg2.is_horizontal():
        if seg1.is_horizontal():
            return find_intersections_perpendicular(seg1, seg2, steps)
        return find_intersections_perpendicular(seg2, seg1, steps)
    axis = seg1.axis
    if seg1.p[1 - axis] == seg2.p[1 - axis]:
        return find_intersections_coincident(seg1, seg2, steps, axis)
    return []

with open(r'inputs\03.txt') as f:
    paths = []
    for line in f:
        paths.append(line.rstrip().split(','))

wires = []
for i in range(len(paths)):
    wires.append(Wire())
    for cmd in paths[i]:
        wires[i].extend_path(cmd)

intersections = []
wire1, wire2 = wires

for i in range(len(wire1.path)):
    for j in range(len(wire2.path)):
        intersections.extend(find_intersections(
            wire1.path[i], wire2.path[j], wire1.steps[i] + wire2.steps[j]))

print('Part 1 answer:', min(i[1] for i in intersections))
print('Part 2 answer:', min(i[2] for i in intersections))
