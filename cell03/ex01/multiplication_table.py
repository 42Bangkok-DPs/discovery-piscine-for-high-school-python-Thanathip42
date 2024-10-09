#!/usr/bin/env python3

number = int(input('Enter a number\n'))

i = 0

while i <= 9:
    result = i * number
    print(str(i) + ' x ' + str(number) + ' = ' + str(result))
    i += 1