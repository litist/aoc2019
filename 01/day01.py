import math


def getFuel(mass):
    return math.floor(mass/3.0) - 2


print(getFuel(100756))


fuel = 0
with open('01/input') as f:
    content = f.readlines()

for mass in content:
    fuel += getFuel(int(mass))
    # print("mass: {} fuel: {} \n".format(int(mass), getFuel(int(mass))))

print("Result: %d", fuel)



def getFuelFuel(mass):
    fuel = 0
    mass = getFuel(mass)
    while mass > 0:
        fuel += mass
        mass = getFuel(mass)

    return fuel

#print("Check 2", getFuelFuel(100756))

fuel = 0
for mass in content:
    fuel += getFuelFuel(int(mass))

print("Result 2: %d", fuel)
