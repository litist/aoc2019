import math
import numpy as np
import matplotlib.pyplot as plt
import copy
import time

filename = '14/input'


converter = {}

with open(filename) as f:
    content = f.readlines()
    for c in content:
        (in_mat, out_mat) = c.split('=>')

        (mult, out_name) = out_mat.strip().split(' ')

        converter[out_name] = [int(mult)]

        for i_chain in in_mat.split(','):

            (mult, in_name) = i_chain.strip().split(' ')

            converter[out_name].append((int(mult), in_name))



mats = {}
mats['ORE'] = 0
mats['FUEL'] = 0

mats_consumed = {}
mats_consumed['ORE'] = 0
mats_consumed['FUEL'] = 0

ore_used = 0


def getMats2(mats_we_want, mats_quant, mats_we_have):
    global ore_used

    if mats_we_want == 'ORE':
        mats_we_have[mats_we_want] += mats_quant
        ore_used += mats_quant
        return

    if not mats_we_want in mats_we_have:
        mats_we_have[mats_we_want] = 0

    if not mats_we_want in mats_consumed:
        mats_consumed[mats_we_want] = 0


    # check for conversion
    conv = converter[mats_we_want]

    # get number of transformations needed
    n_transforms = math.ceil((mats_quant - mats_we_have[mats_we_want]) / conv[0])

    for c in conv[1:]:
        n_el = n_transforms * c[0]
        getMats2(c[1], n_el, mats_we_have)
        # remove mats from list
        mats_we_have[c[1]] -= n_el

        mats_consumed[c[1]] += n_el


    # add to generated mats
    mats_we_have[mats_we_want] += conv[0]*n_transforms


getMats2('FUEL', 1, mats)
print("We used {} ORE to generate 1 FUEL".format(ore_used))


# i do not know what could be a good guess for upper limit
upper_limit = 100000000000
lower_limit = 1000000000000 / mats_consumed['ORE']

# make binary search
while True:
    middle = int((upper_limit + lower_limit) / 2)

    if middle == lower_limit:
        print("Solution 2: ", middle)
        break

    # rest stupid global variables
    mats = {}
    mats['ORE'] = 0
    mats['FUEL'] = 0
    mats_consumed = {}
    mats_consumed['ORE'] = 0
    mats_consumed['FUEL'] = 0

    ore_used = 0

    getMats2('FUEL', middle, mats)

    print('To make {} FUEL, we need {} ORE'.format(mats['FUEL'], mats_consumed['ORE']))

    if mats_consumed['ORE'] > 1000000000000:
        upper_limit = middle
    else:
        lower_limit = middle
