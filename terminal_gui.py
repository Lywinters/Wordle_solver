import wordlegame

from util import all_equal, read_file


class TerminalGui:
    """
    A simple GUI to play a game of Wordle on the terminal
    """
    def __init__(self, game: wordlegame.WordleGame):
        """
        Initialize the game
        :param game: An instance of a WordleGame
        """
        self.game = game

    def start(self):
        """
        Start the game and continue until user presses '!quit' or does not want another round after winning.
        :return: None
        """

        given_input = 'start'

        # Endless game loop until user quits
        while given_input != "!quit":
            given_input = input("Next guess: ")
            guess, score = self.game.guess(given_input)
            if score is None:
                print("Not a valid word. Type !quit to end the game.")
            elif all_equal(score):
                    print("You guessed the word!")
                    given_input = input("Want another round Y/N: ")
                    if given_input.lower() == 'n':
                        break
                    else:
                        self.game.reset()
            else:
                print(score)

if __name__ == "__main__":
    secrets_dictionary = read_file("data/wordle_easy.txt")
    full_dictionary = read_file("data/wordle_full.txt")
    test_game = wordlegame.WordleGame(secrets_dictionary, full_dictionary)
    gui = TerminalGui(test_game)
    gui.start()

