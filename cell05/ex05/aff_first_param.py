#!/usr/bin/env python3

import sys

string = sys.argv

if len(sys.argv) > 1:
    print(string[1])
else:
    print("none")