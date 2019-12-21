import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import random

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
            print("Operator position is not supported: ", opId)
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
            # allow access to unpopulated entries
            return self.program[self.rb + self.program[ self.ip + opId ]] if self.rb + self.program[ self.ip + opId ] in self.program else 0

        else:
            print("Unkownd mode")
            exit()


    def writeOperand(self, opId, data):
        if opId < 0 or opId > 3:
            print("Operator position is not supported: ", opId)
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

    def get3Ouput(self):
        # loop until first output
        out1 = None
        while(out1 == None):
            out1 = self.step()

        out2 = None
        while(out2 == None):
            out2 = self.step()

        out3 = None
        while(out3 == None):
            out3 = self.step()

        # step until we we reach next out/input or end of program
        while self.getOpCode() != 4 and self.getOpCode() != 3 and not self.finished:
            self.step()

        return [out1, out2, out3]



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

            # reset input
            self.inDate = None

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


content = "109,424,203,1,21101,11,0,0,1106,0,282,21102,18,1,0,1106,0,259,2101,0,1,221,203,1,21101,31,0,0,1106,0,282,21102,1,38,0,1106,0,259,21002,23,1,2,22102,1,1,3,21102,1,1,1,21101,57,0,0,1106,0,303,2101,0,1,222,21002,221,1,3,21001,221,0,2,21102,259,1,1,21102,80,1,0,1106,0,225,21102,1,79,2,21101,0,91,0,1106,0,303,2102,1,1,223,21001,222,0,4,21102,259,1,3,21101,225,0,2,21102,1,225,1,21101,0,118,0,1105,1,225,21002,222,1,3,21101,118,0,2,21101,0,133,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,1,148,0,1105,1,259,1202,1,1,223,20102,1,221,4,20101,0,222,3,21102,1,22,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,1,195,0,105,1,109,20207,1,223,2,21002,23,1,1,21101,-1,0,3,21102,214,1,0,1106,0,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,22101,0,-3,1,22102,1,-2,2,21201,-1,0,3,21101,0,250,0,1105,1,225,22101,0,1,-4,109,-5,2105,1,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22102,1,-2,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21102,343,1,0,1106,0,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21102,384,1,0,1105,1,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,22101,0,1,-4,109,-5,2106,0,0"

program = {}
key = 0
for x in content.split(','):
    program[key] = int(x)
    key += 1

code = IntcodeComputer(program)


def getRes(code, x, y):
    code.reset()

    while code.getOpCode() != 3 and not code.finished:
        code.step()

    code.inDate = x
    code.step()

    while code.getOpCode() != 3 and not code.finished:
        code.step()

    code.inDate = y
    code.step()

    # run to next output
    while code.getOpCode() != 4 and not code.finished:
        code.step()

    return code.step()


l_grid = np.zeros((1400,1400), dtype=int)
l_grid.fill(-1)


# start values
test_x = 500
test_y = 400

plt.figure()

step_size = 1

for i in range(1000):

    # check center point
    a = getRes(code, test_x, test_y)
    l_grid[test_y][test_x] = a

    if a == 0:
        print('this must not happen')
        break

    # check if right corner is in
    a = getRes(code, test_x + 99, test_y)
    l_grid[test_y][test_x + 99] = a

    if a == 0:
        # mode down
        test_y += step_size

        # check if ref point is still in
        c = getRes(code, test_x, test_y)
        l_grid[test_y][test_x] = c

        if c == 0:
            # revert change
            test_y -= step_size


    # check if right corner is in
    b = getRes(code, test_x, test_y + 99)
    l_grid[test_y + 99][test_x] = a

    if b == 0:
        # mode right
        test_x += step_size

        # check if ref point is still in
        c = getRes(code, test_x, test_y)
        l_grid[test_y][test_x] = c

        if c == 0:
            # revert change
            test_x -= step_size

    # done
    if a == 1 and b == 1:
        break


for i in range(-3, 3, 1):
    for j in range(-3, 3, 1):
        l_grid[test_y+j][test_x+i+99] = getRes(code, test_x+i+99, test_y+j)
        l_grid[test_y+j+99][test_x+i] = getRes(code, test_x+i, test_y+j+99)

plt.subplot(121)
plt.imshow(l_grid[400:test_y+120, 500:test_x+120])


plt.subplot(122)
plt.imshow(l_grid[test_y-50:test_y+150, test_x-50:test_x+150])
#plt.savefig("/media/ramdisk/sol1.png")
plt.savefig("19/sol2.png")


# 921745 is too low
print("Solution 2: ", test_x*10000+test_y)


grid = np.zeros((50,50), dtype=int)

for y in range(len(grid)):
    for x in range(len(grid[0])):
        grid[y][x] = getRes(code, x, y)


plt.figure()
plt.imshow(grid)
plt.title('Tractor Beam')
plt.savefig("19/sol1.png")

print("Solution 1: ", np.sum(grid))
