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


content = "1,330,331,332,109,3564,1102,1182,1,15,1101,0,1449,24,1002,0,1,570,1006,570,36,101,0,571,0,1001,570,-1,570,1001,24,1,24,1106,0,18,1008,571,0,571,1001,15,1,15,1008,15,1449,570,1006,570,14,21102,58,1,0,1105,1,786,1006,332,62,99,21101,333,0,1,21102,1,73,0,1106,0,579,1101,0,0,572,1102,1,0,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,1001,574,0,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1105,1,81,21102,340,1,1,1106,0,177,21102,477,1,1,1105,1,177,21101,0,514,1,21101,176,0,0,1106,0,579,99,21102,1,184,0,1105,1,579,4,574,104,10,99,1007,573,22,570,1006,570,165,102,1,572,1182,21102,375,1,1,21102,1,211,0,1106,0,579,21101,1182,11,1,21102,222,1,0,1105,1,979,21101,388,0,1,21101,233,0,0,1105,1,579,21101,1182,22,1,21102,1,244,0,1105,1,979,21102,1,401,1,21102,255,1,0,1105,1,579,21101,1182,33,1,21102,1,266,0,1106,0,979,21102,1,414,1,21102,1,277,0,1105,1,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21102,1,1182,1,21101,313,0,0,1105,1,622,1005,575,327,1102,1,1,575,21102,1,327,0,1105,1,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,36,16,0,109,4,1202,-3,1,586,21001,0,0,-1,22101,1,-3,-3,21102,0,1,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1105,1,597,109,-4,2105,1,0,109,5,2102,1,-4,629,21002,0,1,-2,22101,1,-4,-4,21101,0,0,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,652,21001,0,0,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21102,1,702,0,1106,0,786,21201,-1,-1,-1,1106,0,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21102,731,1,0,1106,0,786,1106,0,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21102,756,1,0,1106,0,786,1105,1,774,21202,-1,-11,1,22101,1182,1,1,21101,0,774,0,1105,1,622,21201,-3,1,-3,1106,0,640,109,-5,2106,0,0,109,7,1005,575,802,20102,1,576,-6,20102,1,577,-5,1105,1,814,21101,0,0,-1,21101,0,0,-5,21101,0,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,45,-3,22201,-6,-3,-3,22101,1449,-3,-3,1201,-3,0,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21102,1,1,-1,1106,0,924,1205,-2,873,21101,0,35,-4,1106,0,924,1201,-3,0,878,1008,0,1,570,1006,570,916,1001,374,1,374,2102,1,-3,895,1102,2,1,0,2102,1,-3,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,921,21002,0,1,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,45,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,47,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1101,0,1,575,21101,0,973,0,1105,1,786,99,109,-7,2106,0,0,109,6,21102,1,0,-4,21101,0,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1106,0,1041,21101,0,-4,-2,1105,1,1041,21102,-5,1,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,1201,-2,0,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,2101,0,-2,0,1105,1,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1106,0,989,21102,1,439,1,1105,1,1150,21101,0,477,1,1105,1,1150,21102,1,514,1,21101,1149,0,0,1105,1,579,99,21102,1157,1,0,1106,0,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,2101,0,-5,1176,1201,-4,0,0,109,-6,2105,1,0,36,9,36,1,7,1,36,1,7,1,36,1,7,1,24,7,5,1,7,1,24,1,5,1,5,1,7,1,24,1,5,1,1,13,24,1,5,1,1,1,3,1,32,1,5,1,1,1,3,7,26,1,5,1,1,1,9,1,26,1,5,1,1,1,9,1,26,1,5,1,1,1,9,1,26,9,9,1,32,1,11,1,32,1,11,1,32,1,11,1,32,7,5,1,44,1,44,1,44,1,36,9,36,1,22,9,13,1,22,1,7,1,13,1,20,13,9,7,16,1,1,1,7,1,1,1,9,1,1,1,3,1,10,5,1,1,1,1,7,1,1,1,9,1,1,1,3,1,10,1,3,1,1,1,1,1,7,1,1,1,9,1,1,1,3,1,6,13,7,1,1,1,3,5,1,1,1,5,6,1,3,1,3,1,1,1,9,1,1,1,3,1,3,1,1,1,12,1,3,7,9,13,12,1,7,1,13,1,3,1,3,1,14,1,7,1,13,9,14,1,7,1,17,1,18,9,17,7,44,1,44,1,44,1,42,9,38,1,5,1,38,1,5,1,38,1,5,1,38,1,5,1,38,1,5,1,38,1,5,1,38,1,5,1,38,7,6"


program = {}
key = 0
for x in content.split(','):
    program[key] = int(x)
    key += 1

code = IntcodeComputer(program)


# read in 
grid = []
while not code.finished:

    # run to next output
    while code.getOpCode() != 4 and not code.finished:
        code.step()

    grid.append(code.step())


# last entry is a None, we remove it
# we also have an additional 10
p = np.array(grid[:-2])

# get positon of linebreaks
linebreaks = np.where(p == 10)

grid = np.reshape(p, (-1, linebreaks[0][0] + 1))
# remove newlines
grid = grid[:, :-1]

# print grid
for y in range(len(grid)):
    for x in range(len(grid[0])):
        print(chr(grid[y][x]), end='')
    print('')


alignment = 0
# loop over scaffold
scaffold = np.where(grid == 35)
for i in range(len(scaffold[0])):
    y = scaffold[0][i]
    x = scaffold[1][i]

    # there are no intersections at the borders
    if y == 0 or x == 0 or x == len(grid[0]) - 1 or y == len(grid) - 1:
        continue

    # check if each adjacent block has a scaffold
    if grid[y-1][x] != 35 or grid[y+1][x] != 35 or grid[y][x-1] != 35 or grid[y][x+1] != 35:
        continue

    # found a scaffold intersection
    alignment += y*x

    # mark it for the plot
    grid[y][x] = ord('O')


plt.figure()
plt.imshow(grid)
plt.title('Scafford Grid')
plt.savefig("17/sol1.png")

print("Solution 1: ", alignment)


def transferRoutine(routine):

    for c in routine:
        # run to next output
        while code.getOpCode() != 3 and not code.finished:
            code.step()

        code.inDate = ord(c)
        code.step()



code.reset()

# start vacuum robot
code.program[0] = 2

# intput main function
transferRoutine("A,A,B,C,B,A,C,B,C,A\n")

# FUNCTION A
transferRoutine("L,6,R,12,L,6,L,8,L,8\n")
# FUNCTION B
transferRoutine("L,6,R,12,R,8,L,8\n")
# FUNCTION C
transferRoutine("L,4,L,4,L,6\n")

# select videofeed
transferRoutine("n\n")

lastNone = 0
while not code.finished:
    ret = code.step()

    if ret != None:
        #print(chr(ret), end='')
        lastNone = ret

print('Solution 2: ', lastNone)
exit()