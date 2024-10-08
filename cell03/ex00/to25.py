#!/usr/bin/env python3

user_input = int(input('Enter a number less than 25\n'))

if user_input >= 25:
    print('Error')
else:
    while user_input <= 25:
        print('Inside the loop, my variable is', user_input)
        user_input += 1