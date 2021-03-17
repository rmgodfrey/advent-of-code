from math import gcd, sqrt, atan2, degrees
from copy import deepcopy
import itertools
import sys

with open('inputs\\' + sys.argv[1] + '.txt') as f:
    asteroid_map = []
    for row in f:
        asteroid_map.append(list(row.rstrip()))

def asteroid_num(asteroid_map):
    asteroids = 0
    for row in asteroid_map:
        for col in row:
            if col == '#':
                asteroids += 1
    return asteroids

def find_asteroids(coord, asteroid_map, laser=False):

    def find_ratio(ast):
        rel_x = ast[0] - coord[0]
        rel_y = ast[1] - coord[1]
        if (rel_x >= 0 and rel_y > 0) or (rel_x > 0 and rel_y <= 0):
            hemisphere = 0
        else:
            hemisphere = 1
        try:
            return hemisphere, ((ast[1] - coord[1]) / (ast[0] - coord[0]))
        except ZeroDivisionError:
            if ast[1] - coord[1] < 0:
                return hemisphere, float('-inf')
            return hemisphere, float('inf')

    asteroid_map = deepcopy(asteroid_map)
    X, Y = coord
    SIZE = len(asteroid_map)
    X_low, X_high = -X, SIZE - X
    Y_low, Y_high = -Y, SIZE - Y
    asteroids = []
    repeat = True
    while repeat and asteroid_num(asteroid_map) > 1:
        ast_length = len(asteroids)
        for i in range(Y_low, Y_high):
            for j in range(X_low, X_high):
                if gcd(j, i) == 1:
                    i_val = i
                    j_val = j
                    while Y_low <= i_val < Y_high and X_low <= j_val < X_high:
                        Y_coord, X_coord = Y + i_val, X + j_val
                        if asteroid_map[Y_coord][X_coord] == '#':
                            asteroids.append((X_coord, Y_coord))
                            if laser:
                                asteroid_map[Y_coord][X_coord] = '.'
                            break
                        i_val += i
                        j_val += j
        asteroids = (asteroids[:ast_length] 
                     + sorted(asteroids[ast_length:], key=find_ratio))
        repeat = laser
    return asteroids, coord
    
results = []
SIZE = len(asteroid_map)

for Y in range(SIZE):
    for X in range(SIZE):
        if asteroid_map[Y][X] == '#':
            coord = X, Y
            results.append(find_asteroids(coord, asteroid_map))

results.sort(key=lambda x: len(x[0]), reverse=True)

print('Part 1:', len(results[0][0]))

part2 = find_asteroids(results[0][1], asteroid_map, True)[0][
    int(sys.argv[2]) - 1
]
print('Part 2:', part2[0] * 100 + part2[1])
