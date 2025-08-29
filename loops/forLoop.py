import sys  
#pip install terminaltables3
from terminaltables3 import DoubleTable

def main():
    data = []
    try:
        num = int(input("Enter number of Multiplication Table: "))
        multiplied = int(input("Multiplication Table up to what number: "))
        data.append([f"Multiplication table for {num}"])

        for row in range(multiplied + 1):
            inner_list = []
            inner_list.append(multiply(num, row))
            data.append(inner_list)
        
        table = DoubleTable(data)
        table.inner_row_border = True
        table.justify_columns[0] = 'center'
        print(table.table)
    except ValueError:
        sys.exit("Input integer only")

def multiply(num, i):
    return f"{num} x {i} = {num * i}"

if __name__ == "__main__":
    main()