from terminaltables3 import SingleTable

def main():
    data = []
    data.append(["Even Numbers up to 100"])
    i = 0
    while i <= 100:
        if i % 2 ==  0:
            row_list = []
            row_list.append(i)
            data.append(row_list)
        i += 1
    table = SingleTable(data)
    print(table.table)
        
if __name__ == "__main__":
    main()