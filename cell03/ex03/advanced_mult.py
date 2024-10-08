#!/usr/bin/env python3

table = 0

while table <= 10:

    i = 0

    print("Table de " + str(table) + ":", end = " ")
    
    while i <= 10:
        result = i * table
        print(str(result), end = " ")
        i += 1
        
    print()
    table += 1
