orbits = []

with open('input.txt') as f:
    for line in f:
        orbits.append(line.strip())

orbits_by_planet = {}

for orbit in orbits:
    planet1, planet2 = orbit.split(')')
    orbits_by_planet[planet2] = planet1

def orbits_from_COM(planet):
    orbited_planet = orbits_by_planet[planet]
    if orbited_planet in orbits_by_planet.keys():
        return 1 + orbits_from_COM(orbited_planet)
    else:
        return 1

number_of_orbits = 0

for planet in orbits_by_planet.keys():
    number_of_orbits += orbits_from_COM(planet)

print('Part 1 answer:', number_of_orbits)

def find_orbiting_planets(planet, planet_dict):
    result = []
    for key in planet_dict:
        if planet_dict[key] == planet:
            result.append(key)
    return result

def find_shortest_path_planets_only(start, end, planet_dict, path=[]):
    path = path + [start]
    if start == 'COM':
        orbited_planet = []
    else:
        orbited_planet = [planet_dict[start]]
    for planet in find_orbiting_planets(start, planet_dict) + orbited_planet:
        if planet not in path:
            if planet == end:
                return len(path)
            length = find_shortest_path_planets_only(planet, end, planet_dict, path)
            if length != None:
                return length

def find_shortest_path(YOU, SAN, planet_dict=orbits_by_planet):
    start = planet_dict[YOU]
    end = planet_dict[SAN]
    planet_dict = planet_dict.copy()
    del planet_dict[YOU]; del planet_dict[SAN]
    return find_shortest_path_planets_only(start, end, planet_dict)
    
print('Part 2 answer:', find_shortest_path('YOU', 'SAN'))