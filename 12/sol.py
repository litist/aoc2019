import math
import numpy as np
import copy


def getCycleOneCoord(a,b,c,d):
    moons = np.array([a,b,c,d])

    _m = copy.deepcopy(moons)

    velo = np.zeros(4, dtype=int)

    cycles = np.zeros(4, dtype=np.ulonglong)

    steps = 0

    while np.any(cycles == 0):
        steps += 1

        # apply gravity
        for i in range(4):
            velo[i] += np.sum(moons > moons[i]) - np.sum(moons < moons[i])

        # change position
        moons += velo

        if np.all(moons == _m) and np.all(velo == 0):
            return steps



def getCycles(a, b, c, d):
    moons = np.array([a,b,c,d])

    _m = copy.deepcopy(moons)

    velo = np.zeros([4,3], dtype=int)

    cycles = np.zeros(3, dtype=np.ulonglong)

    for i in range(3):
        cycles[i] = getCycleOneCoord(a[i], b[i], c[i], d[i])

    return np.lcm.reduce(cycles)



def getEnergy(a, b, c, d, steps):
    moons = np.array([a,b,c,d])
    velo = np.zeros([4,3], dtype=int)

    locations = np.zeros([4,400,400])


    for step in range(steps):
        # apply gravity
        for i in range(4):
            velo[i] += np.sum(moons > moons[i], axis=0) - np.sum(moons < moons[i], axis=0)

        # change position
        moons += velo

        # print(step, moons, velo)

    return np.sum(np.sum(np.abs(moons), axis=1) * np.sum(np.abs(velo), axis=1))


# tests
print(179, getEnergy([-1, 0, 2], [2, -10, -7], [4, -8, 8], [3, 5, -1], 10))
print(1940, getEnergy([-8, -10,-0], [5,5,10], [2,-7,3], [9,-8,-3], 100))

print('Solution 1: ', getEnergy([17, -9, 4],[2, 2, -13],[-1, 5, -1],[4, 7, -7], 1000))


# tests
print(2772, getCycles([-1, 0, 2], [2, -10, -7], [4, -8, 8], [3, 5, -1]))
print(4686774924,  getCycles([-8, -10,-0], [5,5,10], [2,-7,3], [9,-8,-3]))

# Cycles: 231614, 96236, 193052 -> 537881600740876
print('Solution 2: ', getCycles([17, -9, 4],[2, 2, -13],[-1, 5, -1],[4, 7, -7]))
