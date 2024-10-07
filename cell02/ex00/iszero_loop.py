while True:
    user_input = input()

    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break

    try:
        number = float(user_input)
        if number == 0:
            print("This number is equal to zero.")
        else:
            print("This number is different from zero.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")