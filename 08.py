with open(r'inputs\08.txt') as f:
    image = f.read().rstrip()

WIDTH = 25
HEIGHT = 6
DIMENSIONS = WIDTH * HEIGHT

layers = [
    image[i:i + DIMENSIONS] 
    for i in range(0, len(image), DIMENSIONS)
]

smallest = min(layers, key=lambda s: s.count('0'))

print('Part 1:', smallest.count('1') * smallest.count('2'))

decoded = ''
for i in range(DIMENSIONS):
    j = 0
    while True:
        if layers[j][i] == '0':
            decoded += ' '
            break
        if layers[j][i] == '1':
            decoded += '\u2588'
            break
        j += 1

print('Part 2:')
for i in range(0, len(decoded), WIDTH):
    print(decoded[i:i + WIDTH])
