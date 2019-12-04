import math 
res = 0
res_2 = 0

for i in range(147981, 691423 + 1):

    double = False
    atLeastDouble = False

    # get first digit
    d_last = math.floor(i / 100000)

    inARow = 0
    for dig in range(4, -1, -1):

        # get digit
        d = math.floor(i / math.pow(10, dig)) % 10

        if d < d_last:
            double = False
            atLeastDouble = False
            inARow = 0
            break

        if d == d_last:
            inARow += 1
            atLeastDouble = True
        else:
            if inARow == 1:
                double = True
            inARow = 0

        d_last = d

    if atLeastDouble:
        res += 1

    if double or inARow == 1:
        res_2 += 1

# 1790
# 2: 1206
print("Solution: ", res, res_2)