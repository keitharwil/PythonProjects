import sys  
#pip install terminaltables3
from terminaltables3 import AsciiTable

def main():
    try:
        num = int(input("Enter number of Multiplication Table: "))
        for i in range(int(input("Multiplication Table up to what number: "))):
            print(multiply(num, i))
    except ValueError:
        sys.exit("Input integer only")

def multiply(num, i):
    return f"{num} x {i} = {num * i}"


if __name__ == "__main__":
    main()