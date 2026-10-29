import wordle

from util import all_equal

if __name__ == '__main__':
    game = wordle.Wordle()
    given_input = 'start'
    while given_input != "quit":
        given_input = input("Next guess: ")
        output = game.guess(given_input)
        if output[1] is None:
            print("Not a valid word")
        elif all_equal(output[1]):
                print("You guessed the word!")
                given_input = input("Want another round Y/N: ")
                if given_input.lower() == 'n':
                    break
                else:
                    game.reset()
        else:
            print(output[1])

