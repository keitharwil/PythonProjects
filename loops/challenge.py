from random import randint
import math

def main():
    guessing_game()

def guessing_game():
    num_to_guess = randint(1, 100)
    guesses_left = 10
    guess_try = 1
    while True: 
        try:    
            guess = int(input("Guess number from 1-100: "))
            if guess_try == 10:
                print("You've guessed 10 times, goodluck next time!")
                break
            if guess == num_to_guess:
                numbers_guessed(guess_try)
                break
            else:
                guess_try += 1
                guesses_left -= 1
                guess_hint(guess, num_to_guess)
                if guesses_left >= 10:
                    print(f"You have {guesses_left} guesses left ")
                else:
                    print(f"You have {guesses_left} guess left")
                print()
                pass
        except ValueError:
            print("Inputted was not a number, try again")

def numbers_guessed(guess_try):
    match guess_try:
        case 1:
            print(f"You guessed the number on the {guess_try}st try!")
        case 2:
            print(f"You guessed the number on the {guess_try}nd try!")
        case 3:
            print(f"You guessed the number on the {guess_try}rd try!")
        case _:
            print(f"You guessed the number on the {guess_try}th try!")

def guess_hint(guess, num_to_guess):
    if math.isclose(guess, num_to_guess, abs_tol=5):
        print(f"{guess} is close keep trying!")
    else:
        if guess > num_to_guess:
            print(f"{guess} is too high try again")
        elif guess < num_to_guess:
            print(f"{guess} is too low try again")
    
if __name__ == "__main__":
    main()