from pyfiglet import Figlet
import sys
import random

class FigletApp:
    def __init__(self, args):
        self.figlet = Figlet()
        self.args = args

    def validate(self):
        if len(self.args) < 1:
            sys.exit("Too few arguments")
        elif len(self.args) > 3:
            sys.exit("Too many arguments")

        if len(self.args) == 2:
            if self.args[1] not in ("-f", "--font"):
                sys.exit("Argument not valid, use: -f or --font")
            elif "-f" in self.args or "--font" in self.args:
                index = self.args.index("-f") if "-f" in self.args else self.args.index("--font")
                if index + 1 >= len(self.args):
                    sys.exit("Invalid Usage")

        elif len(self.args) == 3:
            if self.args[2] not in (self.figlet.getFonts()):
                sys.exit("Invalid usage")
    
    def ascii_convert(self):
        font = self.figlet.getFonts()
        s = input("Input: ")

        if len(self.args) == 1:
            self.figlet.setFont(font=random.choice(font))
            print(self.figlet.renderText(s))

    def run(self):
        self.validate()
        self.ascii_convert()

if __name__ == "__main__":
    app = FigletApp(sys.argv)
    app.run()