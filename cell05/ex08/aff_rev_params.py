#!/usr/bin/env python3

import sys

parameters = sys.argv[1:]

if len(parameters) < 2:
    print("none")
else:
    for parameters_2 in reversed(parameters):
        print(parameters_2)