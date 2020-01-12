import math
import numpy as np
import matplotlib.pyplot as plt
import copy

filename = '24/input'


with open(filename) as f:
    content = f.readlines()



# part 2
grid = np.zeros((250, len(content), len(content[0].strip())), dtype=int)

for y in range(len(content)):
    for x in range(len(content[y].strip())):
        grid[0][y][x] = 1 if content[y][x]=='#' else 0

for steps in range(200):

    # make backup
    back = copy.deepcopy(grid)

    for level in range(-110, 110):

        # skip level, where adjacent levels are empty
        if np.sum(grid[level-1]) + np.sum(grid[level]) + np.sum(grid[level+1]) == 0:
            continue

        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):

                if y == 2 and x == 2:
                    continue

                n_adj_bugs = 0

                # read top
                if y == 0:
                    # read from previous level
                    n_adj_bugs += back[level-1][1][2]
                elif y == 3 and x == 2:
                    # read from inside
                    n_adj_bugs += (back[level+1][4][0] + back[level+1][4][1] + back[level+1][4][2] + back[level+1][4][3] + back[level+1][4][4])
                else:
                    n_adj_bugs += back[level][y-1][x]

                # read bottom
                if y == 4:
                    # read from previous level
                    n_adj_bugs += back[level-1][3][2]
                elif y == 1 and x == 2:
                    # read from inside
                    n_adj_bugs += (back[level+1][0][0] + back[level+1][0][1] + back[level+1][0][2] + back[level+1][0][3] + back[level+1][0][4])
                else:
                    n_adj_bugs += back[level][y+1][x]

                # read left
                if x == 0:
                    # read from previous level
                    n_adj_bugs += back[level-1][2][1]
                elif x == 3 and y == 2:
                    # read from inside
                    n_adj_bugs += (back[level+1][0][4] + back[level+1][1][4] + back[level+1][2][4] + back[level+1][3][4] + back[level+1][4][4])
                else:
                    n_adj_bugs += back[level][y][x-1]

                # read right
                if x == 4:
                    # read from previous level
                    n_adj_bugs += back[level-1][2][3]
                elif x == 1 and y == 2:
                    # read from inside
                    n_adj_bugs += (back[level+1][0][0] + back[level+1][1][0] + back[level+1][2][0] + back[level+1][3][0] + back[level+1][4][0])
                else:
                    n_adj_bugs += back[level][y][x+1]



                if back[level][y][x] == 1 and n_adj_bugs != 1:
                    # a bug dies
                    grid[level][y][x] = 0

                if back[level][y][x] == 0 and (2 >= n_adj_bugs >= 1):
                    # infection
                    grid[level][y][x] = 1





plt.figure()
plt.subplot(3,1,1)
plt.imshow(grid[-1])
plt.subplot(3,1,2)
plt.imshow(grid[0])
plt.subplot(3,1,3)
plt.imshow(grid[1])
#plt.title('Bugs Grid')
#plt.savefig("/media/ramdisk/sol2_level{}.png".format(steps))
plt.savefig("24/sol2.png")

# 1948
print("Solution 2: ", np.sum(grid))



# part 1
grid = np.zeros((len(content)+2, len(content[0].strip())+2), dtype=int)

for y in range(len(content)):
    for x in range(len(content[y].strip())):
        grid[y+1][x+1] = 0 if content[y][x]=='.' else 1

seen = []

#for steps in range(4):
while True:
    # make backup
    back = copy.deepcopy(grid)

    biodiversity = 0

    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[y])-1):
            n_adj_bugs = back[y][x-1] + back[y][x+1] + back[y-1][x] + back[y+1][x]

            if back[y][x] == 1 and n_adj_bugs != 1:
                # a bug dies
                grid[y][x] = 0

            if back[y][x] == 0 and (2 >= n_adj_bugs >= 1):
                # infection
                grid[y][x] = 1

            biodiversity += grid[y][x]*np.power(2, (y-1)*(len(grid)-2) + x - 1)

    if biodiversity in seen:
        print("Solution 1: ", biodiversity)
            
        plt.figure()
        plt.imshow(grid)
        plt.title('Bugs Grid')
        #plt.savefig("/media/ramdisk/sol1.png")
        plt.savefig("24/sol1.png")
        break

    seen.append(biodiversity)


