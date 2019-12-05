import math

with open('05/input') as f:
    content = f.readlines()

# test case
#content = {"3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"}

for c in content:
    program = ([int(x) for x in c.split(',')])

ip = 0

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
        g = input("Input Op: ") 
        program[program[ip + 1]] = int(g)
        ip += 2

    elif getOpCode(program[ip]) == 4:
        # output
        operand1 = program[program[ip + 1]] if isPositionMode(program[ip], 1) else program[ip + 1]
        print("Output Op: ", operand1)
        ip += 2

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


print("Result: %d", program)
