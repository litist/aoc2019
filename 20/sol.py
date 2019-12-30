import math
import numpy as np
import matplotlib.pyplot as plt
import copy

filename = '20/input'


with open(filename) as f:
    content = f.readlines()
    print(content)


grid = np.zeros((len(content), len(content[0]) - 1), dtype=int)

for i in range(len(grid)):
    for j in range(len(grid[0])):
        grid[i][j] = ord(content[i][j])



def printGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(chr(grid[i][j]), end='')
        print('')



gMin = 65000

# plt.figure()

# plt.imshow(grid)
# plt.title('Dist Grid')
# plt.savefig("20/sol1.png")



def discoverPortals(grid):

    portals = {}
    # 
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not (ord('A') <= grid[y][x] <= ord('Z')):
                continue

            # found one
            ports = []
            ports.append((y,x, grid[y][x]))
            grid[y][x] = 32

            # check to right 
            if (ord('A') <= grid[y][x+1] <= ord('Z')):
                ports.append((y,x+1, grid[y][x+1]))
                grid[y][x+1] = 32


            # check below
            if (ord('A') <= grid[y+1][x] <= ord('Z')):
                ports.append((y+1,x, grid[y+1][x]))
                grid[y+1][x] = 32


            # found on which side the portal is
            if ports[0][0] == ports[1][0]:
                # same y axis

                if grid[ports[0][0]][ports[0][1]-1] == ord('.'):
                    # left side
                    print('left', ports)
                    ports.append((ports[0][0], ports[0][1]-1))

                elif grid[ports[1][0]][ports[1][1]+1] == ord('.'):
                    # right side
                    print('right ', ports)
                    ports.append((ports[1][0], ports[1][1]+1))

                else:
                    print('ERROR') 

            elif ports[0][1] == ports[1][1]:
                # same x axis

                if grid[ports[0][0]-1][ports[0][1]] == ord('.'):
                    # check top side
                    print('top', ports)
                    ports.append((ports[0][0]-1, ports[0][1]))

                elif grid[ports[1][0]+1][ports[1][1]] == ord('.'):
                    # bottim side
                    print('bottom ', ports)
                    ports.append((ports[1][0]+1, ports[1][1]))

                else:
                    print('ERROR')

            else:
                print('ERROR: portals are not aligned')

            p = chr(ports[0][2])+chr(ports[1][2])

            if p in portals:
                portals[p].append(ports)
            else:
                portals[p] = [ports]

    return portals


def portJumps(portals):
    # build a dict with input-output
    port_jumps = {}

    for key in portals:
        if key == 'AA' or key == 'ZZ':
            continue

        port_jumps[(portals[key][0][0][0], portals[key][0][0][1])] = portals[key][1][2]
        port_jumps[(portals[key][0][1][0], portals[key][0][1][1])] = portals[key][1][2]

        port_jumps[(portals[key][1][0][0], portals[key][1][0][1])] = portals[key][0][2]
        port_jumps[(portals[key][1][1][0], portals[key][1][1][1])] = portals[key][0][2]


    return port_jumps



def buildDistMap(grid):
    dist_grid = np.zeros((len(grid), len(grid[0])), dtype=int)
    dist_grid.fill(65000)

    step = 0

    global portals, port_jumps
    dist_grid[portals['AA'][0][2]] = step

    while True:
        cur = np.where(dist_grid == step)

        if len(cur[0]) == 0:
            break

        for i in range(len(cur[0])):

            # check all 4 adjacent fields
            ff=[(0,1), (1,0), (0,-1), (-1,0)]
            for f in range(4):
                y = cur[0][i] + ff[f][0]
                x = cur[1][i] + ff[f][1]

                
                if (y,x) in port_jumps:
                    (y,x) = port_jumps[(y,x)]


                if grid[y][x] == ord('.') and dist_grid[y][x] > step + 1:
                    dist_grid[y][x] = step + 1

        step += 1

    dist_grid[dist_grid == 65000] = -1

    plt.imshow(dist_grid)
    plt.title('Dist Grid')
    plt.savefig("20/sol1.png")


    print('Solution 1: ', dist_grid[portals['ZZ'][0][2]])



portals = discoverPortals(grid)

port_jumps = portJumps(portals)

buildDistMap(grid)




def buildDistMapRec(grid):
    dist_grid = np.zeros((len(grid), len(grid[0]), 400), dtype=int)
    dist_grid.fill(-1)

    step = 0

    global portals, port_jumps
    dist_grid[portals['AA'][0][2]][0] = step

    while True:
        cur = np.where(dist_grid == step)

        if len(cur[0]) == 0:
            break

        if dist_grid[portals['ZZ'][0][2]][0] > -1:
            break

        for i in range(len(cur[0])):

            # check all 4 adjacent fields
            ff=[(0,1), (1,0), (0,-1), (-1,0)]
            for f in range(4):
                y = cur[0][i] + ff[f][0]
                x = cur[1][i] + ff[f][1]
                z = cur[2][i]

                
                if (y,x) in port_jumps:
                    # check if this is inner or outer recursion
                    if y <= 1 or y >= len(grid) - 2 or x <=2 or x >= len(grid[0]) - 2:
                        # this is a jump out of an grid
                        if z == 0:
                            print('Reached outer exit ', y, x)
                            continue

                        # start and end are treaded as walls
                        if (y,x) == portals['AA'][0][2] or (y,x) == portals['ZZ'][0][2]:
                            continue
                        

                        z -= 1
                    else:
                        # we jump into the grid
                        z += 1
                    
                    (y,x) = port_jumps[(y,x)]

                if grid[y][x] == ord('.') and (dist_grid[y][x][z] > step + 1 or dist_grid[y][x][z] == -1):
                    dist_grid[y][x][z] = step + 1

        step += 1

    print('Solution 2: ', dist_grid[portals['ZZ'][0][2]][0])

    plt.figure(figsize=(60,60))
    for fig_id in range(16):
        plt.subplot(4,4,fig_id+1)
        plt.imshow(dist_grid[...,fig_id], vmin=-1, vmax=np.max(dist_grid))
    plt.savefig("20/sol2.png")


buildDistMapRec(grid)
