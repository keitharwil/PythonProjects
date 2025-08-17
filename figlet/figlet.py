from pyfiglet import Figlet
import random
import sys

figlet = Figlet()

def main():

    validate(sys.argv)
    ascii_convert(sys.argv)

def validate(input):
    if len(input) < 1:
        sys.exit("Too few arguments")
    elif len(input) > 3:
        sys.exit("Too many arguments")

    if len(input) == 2:
        if input[1] not in ("-f", "--font"):
            sys.exit("Argument not valid, use: -f or --font")
        elif "-f" in input or "--font" in input:
            index = input.index("-f") if "-f" in input else input.index("--font")
            if index + 1 >= len(input):
                sys.exit("Invalid Usage")

    elif len(input) == 3:
        if input[2] not in (figlet.getFonts()):
            sys.exit("Invalid usage")

def ascii_convert(argument):
    font = figlet.getFonts()
    s = input("Input: ")

    if len(argument) == 1:
        figlet.setFont(font = random.choice(font))
        print(figlet.renderText(s))




main()