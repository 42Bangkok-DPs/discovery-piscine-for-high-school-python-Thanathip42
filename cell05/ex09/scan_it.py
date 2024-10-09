#!/usr/bin/env python3

import sys
import re

if len(sys.argv) != 3:
    print("none")
    sys.exit()

keyword = sys.argv[1]
search_string = sys.argv[2]

matches = re.findall(r'\b' + re.escape(keyword) + r'\b', search_string)

if not matches:
    print("none")
else:
    print(len(matches))