import sys
print(sys.version)

# Recursive Fuel Counter-Upper, only used in Part Two.
def mass_to_fuel(mass):
    result = mass//3 - 2
    if result <= 0:
        return 0
    return result + mass_to_fuel(result)
    
filename = r'inputs\01.txt'

fuel1 = fuel2 = 0
with open(filename) as f:
    for m in f:
        m = int(m)
        fuel1 += m//3 - 2
        fuel2 += mass_to_fuel(m)
print('Part 1 answer:', fuel1)
print('Part 2 answer:', fuel2)
