import math



fuel = 0
with open('06/input') as f:
    content = f.readlines()

orbit_map = {}

for orbit in content:
    [a, b] = orbit.strip().split(')')
    orbit_map[b] = a

print(orbit_map)

direct_orbits = 0
indirect_orbits = 0

for o in orbit_map:
    # print("Find indirect orbints of ", o)
    direct_orbits += 1
    # find origin
    while orbit_map[o] != 'COM':
        # print('\t', o, orbit_map[o])
        o = orbit_map[o]
        indirect_orbits += 1

print("Solution: ", direct_orbits + indirect_orbits)

# build orbit list of 'YOU'
YOU_l = []
o = 'YOU'
while o != 'COM':
    # print('\t', o, orbit_map[o])
    o = orbit_map[o]
    YOU_l.append(o)

print(YOU_l)

o = 'SAN'
san_step = 0
while o != 'COM':

    # check if o is in list of YOU
    if o in YOU_l:
        print('Sol 2: ', YOU_l.index(o) + 1 + san_step - 2)
        break

    o = orbit_map[o]
    san_step += 1


