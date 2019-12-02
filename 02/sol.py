import math



fuel = 0
with open('02/input') as f:
    content = f.readlines()

for c in content:
    program = ([int(x) for x in c.split(',')])

program[1] = 12
program[2] = 2

# test
# program = ([int(x) for x in "1,1,1,4,99,5,6,0,99".split(',')])

pos = 0

while program[pos] != 99:

    if program[pos] == 1:
        program[program[pos + 3]] = program[program[pos + 1]] + program[program[pos + 2]]
    elif program[pos] == 2:
        program[program[pos + 3]] = program[program[pos + 1]] * program[program[pos + 2]]
    else:
        print("Unknown OP-code: ", program[pos])
        break

    pos += 4

print("Result: %d", program)
print("Result: ", program[0])



for noun in range(0, 100):
    for verb in range(0, 100):


        program = ([int(x) for x in content[0].split(',')])

        program[1] = noun
        program[2] = verb

        pos = 0

        while program[pos] != 99:

            if program[pos] == 1:
                program[program[pos + 3]] = program[program[pos + 1]] + program[program[pos + 2]]
            elif program[pos] == 2:
                program[program[pos + 3]] = program[program[pos + 1]] * program[program[pos + 2]]
            else:
                print("Unknown OP-code: ", program[pos])
                break

            pos += 4

        if program[0] == 19690720:
            print("Result 2:", noun, verb, 100*noun + verb)


