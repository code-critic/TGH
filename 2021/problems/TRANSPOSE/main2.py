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

options, args = parser.parse_args()
if options.size is not None:
    random.seed(options.rand + 1234)

    def pick():
        return 1 if random.random() > 0.80 else 0


    a, b = 2, 6

    if options.rand == 2:
        a, b = 6, 10

    if options.rand == 3:
        a, b = 10, 16

    rows, cols = randint(a, b), randint(a, b)

    if options.rand < 3:
        rows = cols


    m = [[pick() for i in range(cols)] for j in range(rows)]


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

print(cols, rows)
printM(m)
exit(0)
