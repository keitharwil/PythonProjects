import sys
import csv

class list:
    def __init__(self, args):
        self.args = args

    def validate(self):
        argc = len(self.args)
        if argc < 2:
            sys.exit("Too few arguments")
        if argc > 2:
            sys.exit("Too many arguments")

        if argc == 1:
            return None
        
        if argc == 2:
            if self.args[1] not in ("-w","--write","-n", "--newlist"):
                sys.exit('Argument not valid, use: "-w" "--write" to write in list or "-n" "--newlist" to create a new one')

    def write(self):
        table = []
        if self.args[1] in ("-w", "--write"):    
            with open("list.csv", "a", newline="") as file:
                writer = csv.writer(file)
                while True:    
                    try:
                        
                        writer.writerow()

                
                


    

