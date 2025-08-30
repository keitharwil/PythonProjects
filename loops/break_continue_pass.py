from collections import Counter

def main():
    print(calculate_input("Input calculation: "))

def calculate_input(prompt):
    operation = []
    while True:
        try:
            operation = str(input(prompt)).split()
            if len(operation) != 3:
                raise ValueError
            return calculate(operation[0], operation[1], operation[2])
        except ValueError:
            print("Invalid operation")
            pass
        except ZeroDivisionError:
            print("Can't divide number by 0")
            break

def calculate(num1, operation, num2):
    try:
        match operation:
            case '+':
                return f"{num1} + {num2} = {int(num1) + int(num2)}"
            case '-':
                return f"{num1} - {num2} = {int(num1) - int(num2)}"
            case 'x':
                return f"{num1} x {num2} = {int(num1) * int(num2)}"
            case '/':
                return f"{num1} / {num2} = {int(num1) / int(num2)}"
            case _:
                raise ValueError 
    except ZeroDivisionError:
        raise ZeroDivisionError
    
if __name__ == "__main__":
    main()
