import math
import copy
import itertools

with open('07/input') as f:
    content = f.readlines()

# test case
#content = {"3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"}
# content = ["3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"]

def getOpCode(code):
    return code % 100

def isPositionMode(code, paramPos):
    return getMode(code, paramPos) == 0

def getMode(code, paramPos):
    # check which mode is used
    mode = math.floor(code / (math.pow(10, paramPos + 1))) % 10

    if mode > 1:
        print("Unknown mode for op: ", code)

    return mode


class MultiAmp:
    def __init__(self, program, phases):
        self._program = program
        self._phases = phases

        self.amps = ([Amp(self._program, p) for p in self._phases])

    
    def setPhases(self, phases):
        self._phases = phases

        for i in range(len(self.amps)):
            self.amps[i].setPhase(self._phases[i])

    # get part 1 of the solution
    def getMax_part1(self, pList):

        max_amp = 0
        for amp_f in itertools.permutations(pList):
            self.setPhases(amp_f)

            # get amplification for only one step
            t_amp = 0
            for amp in self.amps:
                t_amp = amp.step(t_amp)

            if t_amp > max_amp:
                max_amp  = t_amp
                print(t_amp, amp_f)

        return max_amp

    # get amplification when run in loop-back mode
    def getResult(self):
        i_val = 0
        while self.amps[-1].finished == False:
            # run each amplifiert with previous input value
            for amp in self.amps:
                i_val = amp.step(i_val)

        return i_val

    def getMax(self, pList):

        max_amp = 0
        for amp_f in itertools.permutations(pList):
            self.setPhases(amp_f)

            t_amp = self.getResult()
            if t_amp > max_amp:
                max_amp  = t_amp
                print(t_amp, amp_f)

        return max_amp



class Amp:
    def __init__(self, program, phase):
        self._program = program
        self.amp_value = 0
        self.phase = phase
        self.finished = False

        self.ip = 0
        self.cur_prog = copy.deepcopy(self._program)


    def setPhase(self, phase):
        self.phase = phase
        self.amp_value = 0
        self.finished = False
        self.ip = 0

        # reset program
        self.cur_prog = copy.deepcopy(self._program)

    def step(self, input):
        #print("pre", self.cur_prog, self.ip)

        if self.ip == 0:
            #print("First step", [self.phase, input])
            ret = run_amp(self.cur_prog, [self.phase, input], self.ip)
        else:
            ret = run_amp(self.cur_prog, [input], self.ip)

        #print("ret: ", ret)
        #print("post", self.cur_prog, self.ip)

        self.ip = ret[1]

        if ret[0] == None:
            self.finished = True
            #print("Amp is done")
            return self.amp_value

        self.amp_value = ret[0]

        return self.amp_value




def run_amp(program, input, ip):

    input_offset = 0

    while getOpCode(program[ip]) != 99:

        if getOpCode(program[ip]) == 1:
            # addition
            operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
            operand2 = program[program[ip + 2]] if isPositionMode(program[ip], 2) else program[ip + 2]

            program[program[ip + 3]] = operand1 + operand2
            ip += 4

        elif getOpCode(program[ip]) == 2:
            # mulitplication
            operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
            operand2 = program[program[ip + 2]] if isPositionMode(program[ip], 2) else program[ip + 2]

            program[program[ip + 3]] = operand1 * operand2
            ip += 4

        elif getOpCode(program[ip]) == 3:
            # input
            # g = input("Input Op: ") 
            # print("Autoinput: ", input[input_offset])
            program[program[ip + 1]] = int(input[input_offset])
            ip += 2

            input_offset += 1


        elif getOpCode(program[ip]) == 4:
            # output
            operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
            # print("Output Op: ", operand1)
            ip += 2
            return [operand1, ip]

        elif getOpCode(program[ip]) == 5:
            # jump-if-true
            operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
            operand2 = program[program[ip + 2]] if isPositionMode(program[ip], 2) else program[ip + 2]

            # set new instruction pointer or increase as in regeular case
            ip = operand2 if operand1 != 0 else ip + 3

        elif getOpCode(program[ip]) == 6:
            # jump-if-false
            operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
            operand2 = program[program[ip + 2]] if isPositionMode(program[ip], 2) else program[ip + 2]

            # set new instruction pointer or increase as in regeular case
            ip = operand2 if operand1 == 0  else ip + 3

        elif getOpCode(program[ip]) == 7:
            # less than
            operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
            operand2 = program[program[ip + 2]] if isPositionMode(program[ip], 2) else program[ip + 2]

            program[program[ip + 3]] = 1 if operand1 < operand2 else 0

            ip += 4

        elif getOpCode(program[ip]) == 8:
            # equals
            operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
            operand2 = program[program[ip + 2]] if isPositionMode(program[ip], 2) else program[ip + 2]

            program[program[ip + 3]] = 1 if operand1 == operand2 else 0

            ip += 4

        else:
            print("Unknown OP-code: ", program[ip])
            break

    # indicate end of program
    return [None, ip]




program = ([int(x) for x in content[0].split(',')])
ma = MultiAmp(program, [9,8,7,6,5])

print("Solution 1: ", ma.getMax_part1([0,1,2,3,4]))
print("Solution 2: ", ma.getMax([5,6,7,8,9]))
