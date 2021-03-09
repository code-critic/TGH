#!/usr/bin/python
# author:   Jan Hybs

from optparse import OptionParser
from random import randint
import random
import os
import sys
import json


# --------------------------


parser = OptionParser()
parser.add_option(
    "-p", "--program-size",
    dest="size",
    help="program size",
)

parser.add_option(
    "-r",
    dest="rand", type=int,
    help="Use non-deterministic algo",
    default=0
)

# -------------------------- GENERATE

def printM(m):
    print('\n'.join([' '.join([str(j) for j in i]) for i in m]))

def printS(m):
    for i, j in enumerate(m):
        adj = [chr(k+65) for k, l in enumerate(j) if l > 0]
        print(f'{chr(i+65)}:', ' '.join(adj))

options, args = parser.parse_args()
if options.size is not None:
    random.seed(options.rand + 12345)

    rows, cols = 8, 13
    r = 0.8

    if options.rand == 1:
        rows, cols = 4, 4
        r = 0.5

    if options.rand == 2:
        rows, cols = 6, 6
        r = 0.5

    if options.rand == 3:
        rows, cols = 8, 8
        r = 0.8

    def pick():
        return 1 if random.random() > r else 0


    m = [[0 if i == j else pick() for i in range(cols)] for j in range(rows)]


    print(rows, cols)
    printM(m)
    exit(0)

# -------------------------- SOLVE

import sys
rows, cols = sys.stdin.readline().split()
rows, cols = int(rows), int(cols)
m = []
for i in range(rows):
    m.append([int(j) for j in sys.stdin.readline().split()])

# transpose
m = zip(*m)
printS(m)
#printS(m)


# 1: 3
# 2: 1 3
# 3: 1 4
# 4: 2

# 0 0 1 0
# 1 0 1 0
# 1 0 0 1
# 0 1 0 0

# 1: 2 3
# 2: 4
# 3: 1 2
# 4: 3

# 0 1 1 0
# 0 0 0 1
# 1 1 0 0
# 0 0 1 0