import math
import numpy as np
import matplotlib.pyplot as plt
import copy
import time


base_pattern = np.array([0, 1, 0, -1], dtype=int)

content = "59766299734185935790261115703620877190381824215209853207763194576128635631359682876612079355215350473577604721555728904226669021629637829323357312523389374096761677612847270499668370808171197765497511969240451494864028712045794776711862275853405465401181390418728996646794501739600928008413106803610665694684578514524327181348469613507611935604098625200707607292339397162640547668982092343405011530889030486280541249694798815457170337648425355693137656149891119757374882957464941514691345812606515925579852852837849497598111512841599959586200247265784368476772959711497363250758706490540128635133116613480058848821257395084976935351858829607105310340"


# part 2 
# we only generate the required digits
input_signal = np.tile(np.array([int(x) for x in list(content)], dtype=int), 10000)
L = len(input_signal)

message_offset = int(content[:7])

for phase in range(100):

    output_signal = np.zeros(L, dtype=int)

    # fill up digits in reverse order
    running_sum = 0
    for c in range(L-1, message_offset - 1, -1):
        running_sum += input_signal[c]
        output_signal[c] = running_sum % 10

    input_signal = output_signal


print("Solution 2: ", ''.join([str(x) for x in output_signal[message_offset:message_offset+8]]))



# part 1
input_signal = np.array([int(x) for x in list(content)], dtype=int)

L = len(input_signal)

for phase in range(100):

    output_signal = np.zeros(L, dtype=int)

    for c in range(L):

        N_rep = math.ceil( (L + 1) / len(base_pattern) / (c + 1) )
        g_pattern = np.tile(np.repeat(base_pattern, c + 1), N_rep)

        g_pattern = g_pattern[1:L+1]

        o = np.abs(input_signal.dot(g_pattern)) % 10

        output_signal[c] = o

    input_signal = output_signal

print("Solution 1: ", ''.join([str(x) for x in output_signal[:8]]))
