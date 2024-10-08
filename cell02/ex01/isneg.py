#!/usr/bin/env python3

user_input = input()

number = float(user_input)
if number > 0:
    print("This number is positive.")
elif number < 0:
    print("This number is negative.")
else:
    print("This number is both positive and negative.")