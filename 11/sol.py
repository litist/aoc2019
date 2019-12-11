import math
import copy
import numpy as np
import matplotlib.pyplot as plt

class IntcodeComputer:
    def __init__(self, program):
        self._program = program
        self.finished = False
        self.inDate = None

        self.ip = 0
        self.rb = 0 # realtive base
        self.program = copy.deepcopy(self._program)


    def reset(self):
        self.finished = False
        self.ip = 0
        self.rb = 0
        self.inDate = None

        # reset program
        self.program = copy.deepcopy(self._program)

        return self


    def getAddressMode(self, opId):

        # check which mode is used
        mode = math.floor(self.program[self.ip] / (math.pow(10, opId + 1))) % 10

        if mode > 2:
            print("Unknown mode for op: ", self.program[self.ip])

        return mode

    def getOperand(self, opId):

        if opId < 0 or opId > 2:
            print("Operator position is not supported: ", OpId)
            exit()

        mode = self.getAddressMode(opId)

        if mode == 0:
            # positionalMode
            # allow access to unpopulated entries
            return self.program[ self.program[ self.ip + opId ] ] if self.program[ self.ip + opId ] in self.program else 0

        elif mode == 1:
            # immediate mode
            return self.program[self.ip + opId]

        elif mode == 2:
            # relative mode
            return self.program[self.rb + self.program[ self.ip + opId ]]

        else:
            print("Unkownd mode")
            exit()


    def writeOperand(self, opId, data):
        if opId < 0 or opId > 3:
            print("Operator position is not supported: ", OpId)
            exit()

        mode = self.getAddressMode(opId)

        if mode == 0:
            # positionalMode
            # allow access to unpopulated entries
            self.program[ self.program[ self.ip + opId ] ] = data

        elif mode == 1:
            # immediate mode
            print("Immediate mode is not supported in write mode!")
            exit()

        elif mode == 2:
            # relative mode
            self.program[self.rb + self.program[ self.ip + opId ]] = data

        else:
            print("Unkownd mode")
            exit()



    def getOpCode(self):
        return self.program[self.ip] % 100


    def run(self, inputDate=None):
        self.inDate = inputDate

        while(self.getOpCode() != 99):
            self.step()

    def get2Ouput(self, inDate):
        self.inDate = inDate

        # loop until first output
        out1 = None
        while(out1 == None):
            out1 = self.step()

        out2 = None
        while(out2 == None):
            out2 = self.step()

        # step until we we reach next input or end of program
        while self.getOpCode() != 3 and not self.finished:
            self.step()

        return [out1, out2]



    def step(self):
        opCode = self.getOpCode()

        if opCode == 1:
            # addition
            operand1 = self.getOperand(1)
            operand2 = self.getOperand(2)

            self.writeOperand(3, operand1 + operand2)
            self.ip += 4

        elif opCode == 2:
            # mulitplication
            operand1 = self.getOperand(1)
            operand2 = self.getOperand(2)

            self.writeOperand(3, operand1 * operand2)
            self.ip += 4

        elif opCode == 3:
            # input
            if self.inDate == None:
                g = int(input("Input Op: "))
            else:
                g = self.inDate
                # print("Input Op: ", g)

            self.writeOperand(1, g)
            self.ip += 2

        elif opCode == 4:
            # output
            operand1 = self.getOperand(1)
            # print("Output Op: ", operand1)
            self.ip += 2
            return operand1

        elif opCode == 5:
            # jump-if-true
            operand1 = self.getOperand(1)
            operand2 = self.getOperand(2)

            # set new instruction pointer or increase as in regeular case
            self.ip = operand2 if operand1 != 0 else self.ip + 3

        elif opCode == 6:
            # jump-if-false
            operand1 = self.getOperand(1)
            operand2 = self.getOperand(2)

            # set new instruction pointer or increase as in regeular case
            self.ip = operand2 if operand1 == 0  else self.ip + 3

        elif opCode == 7:
            # less than
            operand1 = self.getOperand(1)
            operand2 = self.getOperand(2)

            self.writeOperand(3, 1 if operand1 < operand2 else 0)
            self.ip += 4

        elif opCode == 8:
            # equals
            operand1 = self.getOperand(1)
            operand2 = self.getOperand(2)

            self.writeOperand(3, 1 if operand1 == operand2 else 0)
            self.ip += 4

        elif opCode == 9:
            # adjust relative base
            operand1 = self.getOperand(1)

            self.rb += operand1
            self.ip += 2

        elif opCode == 99:
            self.finished = True
            print("End of program: ")

        else:
            print("Unknown OP-code: ", self.program[self.ip])
            exit()

        return None


content = "3,8,1005,8,315,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,29,2,1006,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,55,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,76,1,101,17,10,1006,0,3,2,1005,2,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,110,1,107,8,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,135,1,108,19,10,2,7,14,10,2,104,10,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,170,1,1003,12,10,1006,0,98,1006,0,6,1006,0,59,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,205,1,4,18,10,1006,0,53,1006,0,47,1006,0,86,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,239,2,9,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,266,1006,0,8,1,109,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,294,101,1,9,9,1007,9,1035,10,1005,10,15,99,109,637,104,0,104,1,21102,936995730328,1,1,21102,1,332,0,1105,1,436,21102,1,937109070740,1,21101,0,343,0,1106,0,436,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,179410308187,1,21101,0,390,0,1105,1,436,21101,0,29195603035,1,21102,1,401,0,1106,0,436,3,10,104,0,104,0,3,10,104,0,104,0,21102,825016079204,1,1,21102,1,424,0,1105,1,436,21102,1,825544672020,1,21102,435,1,0,1106,0,436,99,109,2,21202,-1,1,1,21102,1,40,2,21102,467,1,3,21101,0,457,0,1105,1,500,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,462,463,478,4,0,1001,462,1,462,108,4,462,10,1006,10,494,1102,0,1,462,109,-2,2106,0,0,0,109,4,1202,-1,1,499,1207,-3,0,10,1006,10,517,21102,1,0,-3,22101,0,-3,1,22101,0,-2,2,21101,1,0,3,21101,0,536,0,1106,0,541,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,564,2207,-4,-2,10,1006,10,564,21202,-4,1,-4,1105,1,632,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,583,0,0,1106,0,541,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,602,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,624,21202,-1,1,1,21101,624,0,0,106,0,499,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0"

program = {}
key = 0
for x in content.split(','):
    program[key] = int(x)
    key += 1

code = IntcodeComputer(program)
print("Part 1:")

rot_r = np.array([[0, -1],
                  [1, 0]])

rot_l = np.array([[0, 1],
                  [-1, 0]])



color_grid = np.zeros([150,150], dtype=np.uint8)
visits_grid = np.zeros([150,150], dtype=np.uint32)

pos = np.array([75,75])
direction = np.array([0,-1])

while not code.finished:

    [newColor, turnRight] = code.get2Ouput(color_grid[pos[1], pos[0]])

    color_grid[pos[1], pos[0]] = newColor
    visits_grid[pos[1], pos[0]] += 1

    # change direction
    direction = rot_r.dot(direction) if turnRight else rot_l.dot(direction)
    pos += direction


plt.figure()
plt.subplot(2,1,1)
plt.imshow(color_grid, cmap='binary')
plt.title('Panel Color')

plt.subplot(2,1,2)
plt.imshow(visits_grid)
plt.title('Number of visits')

plt.savefig("11/sol1.png")

print("Solution 1: ", np.sum(visits_grid > 0))


## part 2
code.reset()

color_grid = np.zeros([8,45], dtype=np.uint8)
visits_grid = np.zeros([8,45], dtype=np.uint32)

pos = np.array([1,1])
direction = np.array([0,-1])

# start with a single white panel
color_grid[pos[1], pos[0]] = 1

while not code.finished:

    [newColor, turnRight] = code.get2Ouput(color_grid[pos[1], pos[0]])

    color_grid[pos[1], pos[0]] = newColor
    visits_grid[pos[1], pos[0]] += 1

    # change direction
    direction = rot_r.dot(direction) if turnRight else rot_l.dot(direction)
    pos += direction


plt.figure()
plt.subplot(2,1,1)
plt.imshow(color_grid, cmap='binary')
plt.title('Panel Color')

plt.subplot(2,1,2)
plt.imshow(visits_grid)
plt.title('Number of visits')

plt.savefig("11/sol2.png")
