import random
import math
import numpy as np
from BatAlgorithm import *


def funEasom(d):
    res = 1
    for i in d:
        res = res * math.cos(i) * math.exp(-1.0 * np.sum((np.array(d) - math.pi * np.ones(np.array(d).shape)) ** 2))
    if len(d) % 2 == 0:
        res = -1 * res
    return res

dimensi= 2
n_bat=100
n_generasi=100000
r0=0.1
alpha=0.95
gamma=0.95
fmin=0
fmax=1
b_down =-10
b_up =10

ba = BatAlgorithm(dimensi, n_bat, n_generasi, r0, alpha, gamma, fmin, fmax, b_down, b_up, funEasom)

ba.proses_ba()
