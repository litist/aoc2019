import math
import numpy as np
import matplotlib.pyplot as plt
import copy

filename = '10/input'




# get dimensions of asteroid map

with open(filename) as f:
    content = f.readlines()

    asteroid_map = np.zeros([len(content), len(content[0].strip())], dtype=np.int8)
    
    for y in range(np.size(asteroid_map, 0)):
        for x in range(np.size(asteroid_map, 1)):
            asteroid_map[y, x] = 1 if content[y][x] == '#' else 0










max_reachable = 0

# loop over each asteriod
for check_y in range(np.size(asteroid_map, 0)):
    for check_x in range(np.size(asteroid_map, 1)):

        if asteroid_map[check_y, check_x] != 1:
            continue


        reachable = np.zeros([len(content[0].strip()), len(content)], dtype=np.int8)

        reachable[check_y, check_x] = 2

        # check each other asteroid
        for y in range(np.size(asteroid_map, 0)):
            for x in range(np.size(asteroid_map, 1)):

                if asteroid_map[y, x] != 1 or (check_y == y and check_x == x):
                    continue

                # get dy/dx
                m_nom = (y - check_y)
                m_denom = (x - check_x)

                a = np.gcd(m_nom, m_denom)# if (m_nom != 0 and m_denom !=0 ) else 1

                dm = np.array([m_nom/a, m_denom/a], dtype=np.int)

                check = np.array([check_y, check_x], dtype=np.int) + dm

                hidden = False
                while check[0] >= 0 and check[0] < np.size(asteroid_map, 0) and check[1] >= 0 and check[1] < np.size(asteroid_map, 1):

                    # check if there is an asteroid
                    if asteroid_map[check[0], check[1]] == 1:
                        if hidden:
                            reachable[check[0], check[1]] = -1
                        else:                            
                            reachable[check[0], check[1]] = 1
                            hidden = True

                    check += dm


        if np.sum(reachable == 1) > max_reachable:
            max_reachable = np.sum(reachable == 1)
            print(max_reachable, check_x, check_y)
            sol1 = [max_reachable, check_x, check_y]

            fig, ax = plt.subplots()
            im = ax.imshow(reachable)

            plt.savefig("10/sol1.png")








laser = np.array([sol1[2], sol1[1]], dtype=np.int)

#laser = np.array([3, 8], dtype=np.int)

asteroid_map[laser[0], laser[1]] = 2





angles_dir = []
angles_val = []

# loop over all asteroids to get their angle
for check_y in range(np.size(asteroid_map, 0)):
    for check_x in range(np.size(asteroid_map, 1)):

        if asteroid_map[check_y, check_x] != 1:
            continue

        dy = (check_y - laser[0])
        dx = (check_x - laser[1])

        a = np.gcd(dy, dx)

        dy /= a
        dx /= a

        # p = np.array([check_y, check_x], dtype=np.int8)
        p = np.array([laser[0] + dy, laser[1] + dx], dtype=np.int8)
        

        if not np.any(np.all(angles_dir == p, axis=-1)):
            angles_dir.append(p)
            # add pi/2 to each angle to make the one above the target the lowest one
            # angles_val.append(math.atan(dy/dx) + np.pi/2)
            #angles_val.append( (np.arctan2(dy, dx) + np.pi) % 2*np.pi)
            phi = np.angle(dx + 1j*dy)
            angles_val.append( phi if phi >= -1*np.pi/2 else phi + 2*np.pi )
            #angles_val.append( phi)
            



angle_map = np.zeros(list(asteroid_map.shape))

for i in range(len(angles_dir)):
    angle_map[angles_dir[i][0], angles_dir[i][1]] = angles_val[i]


fig, (ax1, ax2) = plt.subplots(2)

im = ax1.imshow(asteroid_map)
im = ax2.imshow(angle_map)

plt.savefig("10/sol2.png")


## destroy with lasers
sort_indices = np.argsort(angles_val)

asteroid_map_lasered = copy.deepcopy(asteroid_map)
n_destroyed = 1

result_part_2 = 0

while np.sum(asteroid_map_lasered == 1) > 0:
    for i in sort_indices:
        d = angles_dir[i] - laser

        p = np.array([laser[0] + d[0], laser[1] + d[1]], dtype=np.int8)
        # check all position into this direction
        while p[0] >= 0 and p[0] < np.size(asteroid_map_lasered, 0) and p[1] >= 0 and p[1] < np.size(asteroid_map_lasered, 1):
            if asteroid_map_lasered[p[0], p[1]] == 1:
                print("destroy {} at {},{}".format(n_destroyed, p[1], p[0]))
                asteroid_map_lasered[p[0], p[1]] = 0

                if n_destroyed == 200:
                    result_part_2 = 100*p[1] + p[0]

                n_destroyed += 1

                # im = ax2.imshow(asteroid_map_lasered)

                # plt.savefig("10/sol2.png")
                break

            p += d

print("Result 2: ", result_part_2)
