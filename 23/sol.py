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


    def waitInput(self):
        return self.getOpCode() == 3

    def waitOutput(self):
        return self.getOpCode() == 4


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


class NIC:
    def __init__(self, program, address):
        self.code = IntcodeComputer(program)
        self.address = address
        self.queue = []

        self.idle = False

        # set network address
        while not self.code.waitInput() and not self.code.finished:
            self.code.step()

        self.code.inDate = self.address
        self.code.step()


    def packet(self, x, y):
        self.queue.append((x,y))


    def step(self):

        self.idle = False

        # make a few steps and look for input or output data
        #for i in range(50):
        while True:

            if self.code.waitInput() and not self.code.finished:

                if len(self.queue) == 0:
                    self.code.inDate = -1
                    self.code.step()

                    # indicate idle mode
                    self.idle = True
                    return (-1,-1,-1)

                else:
                    self.code.inDate = self.queue[0][0]
                    self.code.step()

                    # wait for next in request
                    while not self.code.waitInput():
                        self.code.step()

                    self.code.inDate = self.queue[0][1]
                    self.code.step()

                    self.queue.pop(0)

                    self.idle = False
                    return (-1,-1,-1)

            
            # check if we output
            if self.code.waitOutput() and not self.code.finished:
                nic_out_0 = None

                nic_out_0 = self.code.step()

                # wait for next out
                while not self.code.waitOutput():
                    self.code.step()
                nic_out_1 = self.code.step()
                
                # wait for next out
                while not self.code.waitOutput():
                    self.code.step()
                nic_out_2 = self.code.step()

                # we are still active
                self.idle = False

                return (nic_out_0, nic_out_1, nic_out_2)


            # main step
            self.code.step()


        return (-1,-1,-1)

                    






content = "3,62,1001,62,11,10,109,2249,105,1,0,2140,1911,1023,1505,1973,1204,1103,674,1742,1474,2218,1167,1773,2072,1058,1942,1235,1536,1332,1806,1134,606,796,2107,736,1678,990,639,1433,2181,837,1268,1606,1878,2004,765,571,901,1299,1367,1837,1569,2035,961,1402,1709,932,868,705,1637,0,0,0,0,0,0,0,0,0,0,0,0,3,64,1008,64,-1,62,1006,62,88,1006,61,170,1106,0,73,3,65,20101,0,64,1,20102,1,66,2,21102,105,1,0,1105,1,436,1201,1,-1,64,1007,64,0,62,1005,62,73,7,64,67,62,1006,62,73,1002,64,2,132,1,132,68,132,1002,0,1,62,1001,132,1,140,8,0,65,63,2,63,62,62,1005,62,73,1002,64,2,161,1,161,68,161,1101,1,0,0,1001,161,1,169,102,1,65,0,1102,1,1,61,1101,0,0,63,7,63,67,62,1006,62,203,1002,63,2,194,1,68,194,194,1006,0,73,1001,63,1,63,1105,1,178,21102,1,210,0,106,0,69,2101,0,1,70,1102,0,1,63,7,63,71,62,1006,62,250,1002,63,2,234,1,72,234,234,4,0,101,1,234,240,4,0,4,70,1001,63,1,63,1106,0,218,1106,0,73,109,4,21101,0,0,-3,21101,0,0,-2,20207,-2,67,-1,1206,-1,293,1202,-2,2,283,101,1,283,283,1,68,283,283,22001,0,-3,-3,21201,-2,1,-2,1106,0,263,21201,-3,0,-3,109,-4,2105,1,0,109,4,21101,1,0,-3,21101,0,0,-2,20207,-2,67,-1,1206,-1,342,1202,-2,2,332,101,1,332,332,1,68,332,332,22002,0,-3,-3,21201,-2,1,-2,1105,1,312,21202,-3,1,-3,109,-4,2106,0,0,109,1,101,1,68,358,21001,0,0,1,101,3,68,366,21002,0,1,2,21101,0,376,0,1105,1,436,21201,1,0,0,109,-1,2105,1,0,1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483648,4294967296,8589934592,17179869184,34359738368,68719476736,137438953472,274877906944,549755813888,1099511627776,2199023255552,4398046511104,8796093022208,17592186044416,35184372088832,70368744177664,140737488355328,281474976710656,562949953421312,1125899906842624,109,8,21202,-6,10,-5,22207,-7,-5,-5,1205,-5,521,21101,0,0,-4,21101,0,0,-3,21101,0,51,-2,21201,-2,-1,-2,1201,-2,385,470,21001,0,0,-1,21202,-3,2,-3,22207,-7,-1,-5,1205,-5,496,21201,-3,1,-3,22102,-1,-1,-5,22201,-7,-5,-7,22207,-3,-6,-5,1205,-5,515,22102,-1,-6,-5,22201,-3,-5,-3,22201,-1,-4,-4,1205,-2,461,1106,0,547,21101,0,-1,-4,21202,-6,-1,-6,21207,-7,0,-5,1205,-5,547,22201,-7,-6,-7,21201,-4,1,-4,1105,1,529,21202,-4,1,-7,109,-8,2105,1,0,109,1,101,1,68,563,21001,0,0,0,109,-1,2106,0,0,1101,29983,0,66,1101,3,0,67,1102,598,1,68,1102,1,302,69,1101,1,0,71,1102,604,1,72,1106,0,73,0,0,0,0,0,0,41,914,1101,0,19759,66,1101,2,0,67,1102,633,1,68,1101,302,0,69,1102,1,1,71,1101,637,0,72,1106,0,73,0,0,0,0,13,16574,1101,65981,0,66,1101,0,3,67,1101,666,0,68,1102,1,302,69,1102,1,1,71,1102,672,1,72,1105,1,73,0,0,0,0,0,0,23,2962,1102,93283,1,66,1101,1,0,67,1101,701,0,68,1102,1,556,69,1101,0,1,71,1101,0,703,72,1106,0,73,1,6381,28,316542,1102,21991,1,66,1102,1,1,67,1102,732,1,68,1101,0,556,69,1102,1,1,71,1101,0,734,72,1106,0,73,1,72610,28,158271,1102,59083,1,66,1102,1,1,67,1101,0,763,68,1101,0,556,69,1102,0,1,71,1102,1,765,72,1105,1,73,1,1321,1101,0,21859,66,1101,0,1,67,1101,0,792,68,1102,1,556,69,1101,0,1,71,1101,0,794,72,1105,1,73,1,4,22,32974,1102,16487,1,66,1102,1,6,67,1101,823,0,68,1101,302,0,69,1102,1,1,71,1102,1,835,72,1105,1,73,0,0,0,0,0,0,0,0,0,0,0,0,41,1828,1101,0,39761,66,1102,1,1,67,1102,864,1,68,1101,556,0,69,1102,1,1,71,1101,866,0,72,1105,1,73,1,29,11,160526,1101,7297,0,66,1101,2,0,67,1101,895,0,68,1102,1,302,69,1102,1,1,71,1101,899,0,72,1106,0,73,0,0,0,0,27,65981,1102,1,40351,66,1102,1,1,67,1102,1,928,68,1101,0,556,69,1102,1,1,71,1102,1,930,72,1106,0,73,1,97,22,98922,1101,1693,0,66,1102,1,1,67,1102,959,1,68,1102,556,1,69,1101,0,0,71,1102,961,1,72,1106,0,73,1,1200,1102,1,1759,66,1102,1,1,67,1102,988,1,68,1101,0,556,69,1101,0,0,71,1102,990,1,72,1106,0,73,1,1465,1101,0,49667,66,1101,1,0,67,1102,1,1017,68,1101,556,0,69,1101,2,0,71,1101,1019,0,72,1106,0,73,1,6163,22,16487,29,359132,1102,1,7591,66,1101,3,0,67,1101,1050,0,68,1102,302,1,69,1102,1,1,71,1101,1056,0,72,1105,1,73,0,0,0,0,0,0,41,1371,1102,1,39373,66,1101,1,0,67,1101,0,1085,68,1102,1,556,69,1101,0,8,71,1101,0,1087,72,1105,1,73,1,1,12,55469,17,58897,33,4261,16,87562,11,80263,38,35053,18,99289,29,179566,1101,0,39551,66,1101,0,1,67,1102,1,1130,68,1102,556,1,69,1101,1,0,71,1101,1132,0,72,1106,0,73,1,125,42,198788,1101,59863,0,66,1102,1,1,67,1102,1,1161,68,1101,556,0,69,1101,0,2,71,1101,1163,0,72,1106,0,73,1,10,42,149091,40,102513,1101,80263,0,66,1102,1,4,67,1102,1194,1,68,1101,302,0,69,1102,1,1,71,1102,1,1202,72,1105,1,73,0,0,0,0,0,0,0,0,13,24861,1102,1,32363,66,1102,1,1,67,1101,0,1231,68,1102,556,1,69,1101,0,1,71,1102,1233,1,72,1106,0,73,1,3,21,19759,1101,43781,0,66,1101,0,2,67,1101,0,1262,68,1101,0,302,69,1102,1,1,71,1102,1266,1,72,1105,1,73,0,0,0,0,22,49461,1102,74597,1,66,1102,1,1,67,1102,1,1295,68,1102,556,1,69,1102,1,1,71,1102,1297,1,72,1105,1,73,1,160,40,205026,1102,1,35053,66,1101,0,2,67,1101,1326,0,68,1101,302,0,69,1102,1,1,71,1101,0,1330,72,1106,0,73,0,0,0,0,18,297867,1101,99289,0,66,1101,3,0,67,1101,0,1359,68,1101,302,0,69,1101,1,0,71,1101,0,1365,72,1105,1,73,0,0,0,0,0,0,13,8287,1101,51287,0,66,1102,1,1,67,1102,1,1394,68,1101,0,556,69,1101,0,3,71,1102,1396,1,72,1105,1,73,1,5,42,49697,42,99394,40,136684,1101,0,5693,66,1102,1,1,67,1102,1429,1,68,1101,0,556,69,1101,1,0,71,1101,0,1431,72,1105,1,73,1,-1452,28,52757,1101,52757,0,66,1101,6,0,67,1101,0,1460,68,1101,253,0,69,1101,0,1,71,1102,1472,1,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,0,0,21,39518,1101,0,15787,66,1101,1,0,67,1101,0,1501,68,1102,1,556,69,1102,1,1,71,1101,0,1503,72,1106,0,73,1,20,18,198578,1101,0,98299,66,1102,1,1,67,1101,1532,0,68,1101,556,0,69,1101,0,1,71,1102,1534,1,72,1106,0,73,1,29289,28,263785,1102,1,58897,66,1102,1,2,67,1101,1563,0,68,1102,302,1,69,1101,0,1,71,1102,1567,1,72,1105,1,73,0,0,0,0,33,8522,1101,0,457,66,1102,4,1,67,1102,1,1596,68,1101,253,0,69,1101,0,1,71,1101,1604,0,72,1106,0,73,0,0,0,0,0,0,0,0,45,71059,1101,23173,0,66,1102,1,1,67,1102,1,1633,68,1102,556,1,69,1101,1,0,71,1101,1635,0,72,1106,0,73,1,-3,29,269349,1101,0,4673,66,1102,1,1,67,1102,1,1664,68,1102,556,1,69,1102,1,6,71,1101,1666,0,72,1106,0,73,1,2,22,82435,47,7297,27,197943,29,89783,40,34171,40,170855,1102,90173,1,66,1101,1,0,67,1101,1705,0,68,1101,0,556,69,1101,0,1,71,1101,1707,0,72,1106,0,73,1,34693,12,110938,1101,71059,0,66,1102,1,2,67,1101,0,1736,68,1101,0,351,69,1102,1,1,71,1102,1740,1,72,1106,0,73,0,0,0,0,255,22469,1102,1,71263,66,1101,1,0,67,1102,1769,1,68,1102,1,556,69,1102,1,1,71,1102,1,1771,72,1106,0,73,1,11,22,65948,1102,1,55469,66,1102,1,2,67,1102,1800,1,68,1101,302,0,69,1102,1,1,71,1101,1804,0,72,1106,0,73,0,0,0,0,17,117794,1102,97961,1,66,1102,1,1,67,1102,1,1833,68,1101,0,556,69,1101,1,0,71,1102,1,1835,72,1105,1,73,1,-5377,28,211028,1102,34171,1,66,1101,0,6,67,1101,1864,0,68,1101,0,302,69,1102,1,1,71,1102,1876,1,72,1105,1,73,0,0,0,0,0,0,0,0,0,0,0,0,45,142118,1102,4261,1,66,1102,2,1,67,1102,1905,1,68,1101,0,302,69,1101,0,1,71,1101,1909,0,72,1105,1,73,0,0,0,0,16,43781,1102,21587,1,66,1102,1,1,67,1101,0,1938,68,1102,556,1,69,1102,1,1,71,1102,1940,1,72,1106,0,73,1,179,27,131962,1101,36373,0,66,1102,1,1,67,1102,1969,1,68,1102,556,1,69,1101,1,0,71,1101,0,1971,72,1105,1,73,1,-404,11,321052,1101,0,69593,66,1101,1,0,67,1101,0,2000,68,1102,556,1,69,1102,1,1,71,1101,2002,0,72,1106,0,73,1,16948,28,105514,1102,15569,1,66,1101,1,0,67,1101,2031,0,68,1102,1,556,69,1101,1,0,71,1101,2033,0,72,1106,0,73,1,71153,38,70106,1102,1,49697,66,1102,1,4,67,1101,0,2062,68,1102,1,302,69,1101,0,1,71,1102,1,2070,72,1106,0,73,0,0,0,0,0,0,0,0,40,68342,1101,0,8287,66,1101,0,3,67,1101,0,2099,68,1102,253,1,69,1102,1,1,71,1101,0,2105,72,1106,0,73,0,0,0,0,0,0,47,14594,1101,1481,0,66,1102,2,1,67,1101,0,2134,68,1101,302,0,69,1102,1,1,71,1101,2138,0,72,1105,1,73,0,0,0,0,41,457,1101,22469,0,66,1102,1,1,67,1101,2167,0,68,1101,556,0,69,1101,0,6,71,1101,2169,0,72,1106,0,73,1,19770,23,1481,36,29983,36,59966,2,7591,2,15182,2,22773,1102,89783,1,66,1102,1,4,67,1102,2208,1,68,1101,0,302,69,1102,1,1,71,1101,0,2216,72,1106,0,73,0,0,0,0,0,0,0,0,36,89949,1102,1,11987,66,1102,1,1,67,1101,2245,0,68,1102,556,1,69,1102,1,1,71,1102,1,2247,72,1106,0,73,1,14,11,240789"

program = {}
key = 0
for x in content.split(','):
    program[key] = int(x)
    key += 1

code = IntcodeComputer(program)

network = []
for i in range(50):
    network.append(NIC(program, i))

nat = (None, None)#NIC(program, 255)



last_nat_y = -1
lastIdle = False
while True:

    for i in range(len(network)):

        (a,x,y) = network[i].step()

        if a >= 0:
            print('{} -> {} : ({},{})'.format(i, a, x, y))

            if a == 255:
                nat = (x,y)
            else:
                network[a].packet(x,y)
    # check if network is idle
    allIdle = True
    for i in range(len(network)):
        allIdle = allIdle and network[i].idle

    if lastIdle and allIdle:
        print('NAT sends to 0: ', nat[0], nat[1])
        network[0].packet(nat[0], nat[1])

        if last_nat_y == nat[1]:
            print('Solution 2: ', last_nat_y)
            exit(1)

        last_nat_y = nat[1]

    lastIdle = allIdle

