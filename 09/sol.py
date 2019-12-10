import math
import copy


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


    def step(self):
        opCode = self.getOpCode()

        if opCode == 99:
            print("Unexpected end of program: ")
            exit()

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
                print("Input Op: ", g)

            self.writeOperand(1, g)
            self.ip += 2

        elif opCode == 4:
            # output
            operand1 = self.getOperand(1)
            print("Output Op: ", operand1)
            self.ip += 2

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

        else:
            print("Unknown OP-code: ", self.program[self.ip])
            exit()



content = "1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,1,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,641,1026,1101,0,24,1014,1101,30,0,1015,1101,0,0,1020,1101,35,0,1000,1101,0,708,1029,1101,0,27,1009,1102,38,1,1007,1102,638,1,1027,1101,1,0,1021,1102,32,1,1003,1101,0,34,1012,1102,20,1,1017,1102,1,37,1010,1101,0,713,1028,1101,33,0,1019,1102,1,36,1001,1102,22,1,1005,1101,23,0,1018,1101,21,0,1016,1102,28,1,1006,1101,0,26,1011,1102,1,215,1022,1102,1,29,1013,1102,25,1,1004,1102,1,31,1008,1102,1,292,1025,1102,297,1,1024,1101,208,0,1023,1102,1,39,1002,109,12,1206,9,197,1001,64,1,64,1106,0,199,4,187,1002,64,2,64,109,11,2105,1,0,1001,64,1,64,1105,1,217,4,205,1002,64,2,64,109,2,21107,40,41,-9,1005,1016,235,4,223,1105,1,239,1001,64,1,64,1002,64,2,64,109,-28,1207,3,36,63,1005,63,261,4,245,1001,64,1,64,1105,1,261,1002,64,2,64,109,5,1207,1,31,63,1005,63,281,1001,64,1,64,1105,1,283,4,267,1002,64,2,64,109,22,2105,1,0,4,289,1105,1,301,1001,64,1,64,1002,64,2,64,109,-16,1201,0,0,63,1008,63,31,63,1005,63,323,4,307,1106,0,327,1001,64,1,64,1002,64,2,64,109,18,1205,-5,345,4,333,1001,64,1,64,1105,1,345,1002,64,2,64,109,-21,2101,0,-2,63,1008,63,32,63,1005,63,367,4,351,1106,0,371,1001,64,1,64,1002,64,2,64,109,6,21102,41,1,7,1008,1018,38,63,1005,63,395,1001,64,1,64,1105,1,397,4,377,1002,64,2,64,109,-1,21107,42,41,2,1005,1012,413,1106,0,419,4,403,1001,64,1,64,1002,64,2,64,109,-10,2107,36,0,63,1005,63,435,1106,0,441,4,425,1001,64,1,64,1002,64,2,64,109,9,21108,43,44,9,1005,1018,461,1001,64,1,64,1105,1,463,4,447,1002,64,2,64,109,-10,2102,1,8,63,1008,63,39,63,1005,63,483,1105,1,489,4,469,1001,64,1,64,1002,64,2,64,109,21,21108,44,44,-1,1005,1019,511,4,495,1001,64,1,64,1106,0,511,1002,64,2,64,109,-18,1208,1,32,63,1005,63,533,4,517,1001,64,1,64,1105,1,533,1002,64,2,64,109,5,2101,0,-5,63,1008,63,37,63,1005,63,557,1001,64,1,64,1105,1,559,4,539,1002,64,2,64,109,8,1208,-8,35,63,1005,63,575,1105,1,581,4,565,1001,64,1,64,1002,64,2,64,109,-5,1202,-3,1,63,1008,63,38,63,1005,63,607,4,587,1001,64,1,64,1106,0,607,1002,64,2,64,109,-17,2107,31,10,63,1005,63,629,4,613,1001,64,1,64,1106,0,629,1002,64,2,64,109,31,2106,0,3,1105,1,647,4,635,1001,64,1,64,1002,64,2,64,109,-7,1201,-9,0,63,1008,63,32,63,1005,63,667,1106,0,673,4,653,1001,64,1,64,1002,64,2,64,109,-5,1202,-5,1,63,1008,63,41,63,1005,63,693,1105,1,699,4,679,1001,64,1,64,1002,64,2,64,109,16,2106,0,0,4,705,1105,1,717,1001,64,1,64,1002,64,2,64,109,-6,1205,-2,729,1105,1,735,4,723,1001,64,1,64,1002,64,2,64,109,-18,2102,1,1,63,1008,63,22,63,1005,63,761,4,741,1001,64,1,64,1105,1,761,1002,64,2,64,109,-2,2108,32,1,63,1005,63,783,4,767,1001,64,1,64,1105,1,783,1002,64,2,64,109,13,21102,45,1,-2,1008,1013,45,63,1005,63,809,4,789,1001,64,1,64,1105,1,809,1002,64,2,64,109,-13,2108,24,3,63,1005,63,829,1001,64,1,64,1106,0,831,4,815,1002,64,2,64,109,13,21101,46,0,-3,1008,1012,43,63,1005,63,851,1106,0,857,4,837,1001,64,1,64,1002,64,2,64,109,14,1206,-9,875,4,863,1001,64,1,64,1106,0,875,1002,64,2,64,109,-3,21101,47,0,-7,1008,1019,47,63,1005,63,901,4,881,1001,64,1,64,1105,1,901,4,64,99,21101,27,0,1,21101,0,915,0,1106,0,922,21201,1,66926,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1105,1,922,21202,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1106,0,968,22102,1,-2,-2,109,-3,2106,0,0"

program = {}
key = 0
for x in content.split(','):
    program[key] = int(x)
    key += 1

day9_part1 = IntcodeComputer(program)
print("Part 1:")
day9_part1.run(1)

print("Part 2:")
day9_part1.reset().run(2)


# this tests if we are still compatible, by checking the tests and the code from day 5
exit()


program = {}
key = 0
for x in "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(','):
    program[key] = int(x)
    key += 1

day9_tes1 = IntcodeComputer(program)
day9_tes1.run()


program = {}
key = 0
for x in "1102,34915192,34915192,7,4,7,99,0".split(','):
    program[key] = int(x)
    key += 1

day9_tes2 = IntcodeComputer(program)
day9_tes2.run()


program = {}
key = 0
for x in "104,1125899906842624,99".split(','):
    program[key] = int(x)
    key += 1

day9_tes3 = IntcodeComputer(program)
day9_tes3.run()


with open('05/input') as f:
    content = f.readlines()

for c in content:
    program = ([int(x) for x in c.split(',')])


day5 = IntcodeComputer(program)

day5.reset().run(1)

day5.reset().run(5)






