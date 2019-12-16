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


content = "3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,102,1,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1106,0,124,1002,1034,1,1039,1001,1036,0,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,1001,1035,0,1040,1002,1038,1,1043,101,0,1037,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,102,1,1035,1040,1001,1038,0,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,1,1032,1006,1032,165,1008,1040,9,1032,1006,1032,165,1102,1,2,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,35,1044,1106,0,224,1101,0,0,1044,1105,1,224,1006,1044,247,102,1,1039,1034,1002,1040,1,1035,1002,1041,1,1036,102,1,1043,1038,101,0,1042,1037,4,1044,1105,1,0,1,5,41,19,22,1,39,81,29,20,15,82,33,18,45,30,32,55,28,26,70,13,56,32,28,18,3,59,90,11,95,15,85,8,61,25,59,24,34,1,85,5,25,54,57,18,20,54,80,91,28,65,36,12,44,36,13,92,24,56,13,39,69,29,79,10,41,27,23,25,72,20,3,61,15,51,11,12,12,48,10,45,13,29,49,90,30,17,9,41,21,18,7,30,48,17,83,71,4,10,31,10,96,81,77,9,50,39,21,36,33,72,12,3,23,79,18,4,75,17,58,64,8,7,97,60,72,72,1,94,55,42,2,94,2,21,88,19,82,57,96,19,25,27,41,62,15,40,23,61,86,27,73,61,13,46,52,81,12,34,23,73,23,59,1,30,47,9,99,10,37,17,28,98,5,92,73,8,63,4,86,76,79,7,30,68,28,91,12,12,98,74,4,22,44,10,23,45,37,16,90,76,23,74,75,12,21,38,14,15,76,28,49,71,7,6,6,71,53,33,12,87,15,92,66,21,38,13,53,92,34,49,25,6,67,21,27,89,24,61,25,30,41,30,99,28,19,41,90,51,74,14,33,54,48,10,14,42,2,67,76,10,21,2,67,43,27,69,11,16,78,7,36,9,24,48,63,81,53,29,94,34,25,99,66,47,17,97,33,52,11,62,22,52,30,23,89,95,15,13,50,48,26,10,6,69,78,13,6,94,1,28,67,10,70,16,50,19,24,15,79,50,27,3,19,62,4,31,83,20,17,83,67,5,80,26,36,62,87,3,10,80,22,65,60,10,78,4,20,60,30,11,7,83,10,13,72,81,37,22,14,55,63,51,27,32,77,52,20,50,16,48,2,55,10,53,26,84,6,87,43,37,26,3,85,62,25,78,50,16,10,37,22,54,5,80,24,7,32,49,18,27,12,41,70,82,20,34,91,15,98,77,22,6,79,3,8,54,17,32,4,44,2,97,14,15,65,30,97,14,79,75,11,77,5,61,37,20,91,20,45,74,19,40,2,41,89,12,34,44,18,62,57,17,68,22,96,7,59,63,2,60,70,2,26,75,26,3,53,19,80,16,97,7,34,58,52,66,24,75,25,30,75,42,13,12,89,13,3,84,92,1,75,30,54,43,2,56,15,1,15,84,99,6,98,42,17,29,1,18,26,70,71,29,91,23,21,87,66,18,38,32,18,81,65,2,58,99,12,4,84,24,32,88,30,67,49,29,59,64,18,70,10,24,56,5,27,97,50,4,28,85,65,16,67,83,15,16,61,18,86,8,36,25,36,29,97,45,19,81,41,29,45,30,69,26,57,93,27,72,34,30,99,61,2,48,16,12,76,98,28,14,32,32,90,48,10,30,57,23,39,2,8,39,33,13,88,34,31,74,15,60,8,47,60,31,5,79,1,98,86,33,3,99,33,62,11,96,25,22,38,98,84,3,56,70,49,3,8,56,87,4,29,59,65,26,34,77,7,14,78,26,25,70,49,3,31,45,92,24,95,17,4,9,4,96,64,92,27,67,4,99,6,44,7,16,86,2,75,1,6,68,81,4,1,44,49,7,92,8,40,36,25,81,13,56,99,10,2,30,72,6,43,30,12,43,93,19,20,23,95,10,19,66,63,28,96,40,50,8,15,56,38,13,93,42,71,12,18,87,8,4,21,85,9,2,66,77,10,80,26,61,9,43,20,88,10,39,67,55,31,49,17,58,26,80,20,84,54,49,5,73,11,52,15,63,7,62,24,57,92,61,25,87,56,37,31,38,14,99,0,0,21,21,1,10,1,0,0,0,0,0,0"

program = {}
key = 0
for x in content.split(','):
    program[key] = int(x)
    key += 1

code = IntcodeComputer(program)


print("Part 1:")

grid = np.zeros([200,200], dtype=np.uint8)

pos = (100,100)

while not code.finished:


    while code.getOpCode() != 3 and not code.finished:
        code.step()


    # random select direction
    direction = random.randint(0,3)
    code.inDate = direction

    print('->', direction)

    while code.getOpCode() != 4 and not code.finished:
        code.step()

    answer = code.step()

    print('<-', answer)

exit()

plt.figure()
# plt.subplot(2,1,1)
# plt.imshow(color_grid, cmap='binary')
# plt.title('Panel Color')

#plt.subplot(2,1,2)
plt.imshow(grid)
plt.title('Number of visits')

plt.savefig("13/sol1.png")

print("Solution 1: ", np.sum(grid == 2))


# part 2
code.reset()

# insert coins
code.program[0] = 2

grid = np.zeros([23,44], dtype=np.uint8)

plt.figure()

frame = 0
score = 0
last_ball_x = 1
while not code.finished:

    if code.getOpCode() == 3:
        if frame % 10 == 0:
            plt.imshow(grid)
            plt.title('Frame: {} Score: {}'.format(frame, score))
            plt.savefig("13/sol1.png")
        frame += 1

        # decide on input
        ball = np.where(grid == 4)
        ball_x = ball[1][0]

        pad = np.where(grid == 3)
        pad_x = pad[1][0]

        dy = pad[0][0] - ball[0][0]

        if last_ball_x < ball_x:
            # ball moves right
            if pad_x <= ball_x:
                # -> move right
                code.inDate = 1

            if pad_x - 1 == ball_x:
                # stay
                code.inDate = 0

            if pad_x - 1 > ball_x:
                # move pad closer  to ball
                code.inDate = -1
        else:
            # ball moves left
            if pad_x >= ball_x:
                # <-
                code.inDate = -1

            if ball_x - 1 == pad_x:
                # stay
                code.inDate = 0

            if ball_x - 1 > pad_x:
                # move pad closer  to ball
                code.inDate = 1

        if dy == 1 and pad_x == ball_x:
            code.inDate = 0

        print('ball: {} pad: {} move: {}'.format(ball_x, pad_x, code.inDate))

        last_ball_x = ball_x

    [x, y, t] = code.get3Ouput()

    if x==-1 and y == 0:
        score = t
        print("Score: ", score)
    else:
        grid[y, x] = t
        

# game over

plt.imshow(grid)
plt.title('Game Over! Frame: {} Score: {}'.format(frame, score))
plt.savefig("13/sol1.png")
