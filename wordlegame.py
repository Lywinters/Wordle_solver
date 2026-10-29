import random
from collections import Counter
from typing import List, Optional, Tuple


class WordleGame:
    """
    An implementation of the Wordle game algorithm. It is a word guessing game, where the player tries to find out the
    secret word in a fixed number of guesses. Each guess gets scored by telling the player which letter of the last
    guess is right for the secret word. The possible scores for each letter are 'x', which means the letter is not in
    the secret word, yellow 'y' which means the letter is in the secret word, but not in the correct position, and
    green 'g' which means the letter is in the secret word and even in the correct position.
    """

    def __init__(self, secrets_dictionary: List[str], full_dictionary: List[str], rng_seed = None) -> None:
        """
        Sets up a Wordle game.
        :param secrets_dictionary: A list of words from which the secret word is randomly chosen.
                                   Each word has to have the same length.
        :param full_dictionary: A list of words that are valid guesses for the game.
                                Each word has to have the same length.
                                The full dictionary has to contain the complete secrets dictionary.
        :param rng_seed: An optional random seed to use for reproducibility.
        """
        self.secrets_dictionary = secrets_dictionary
        self.full_dictionary = full_dictionary
        self.secret_word = None
        self.guesses = []
        random.seed(rng_seed)
        self.word_length = len(self.full_dictionary[0])  # no verification that all words have the same length
        self.order = list(range(len(self.secrets_dictionary)))
        random.shuffle(self.order)  # shuffle the secrets diary to only have to randomize once
        self.secret_word_idx = -1  # index where the secret word is located in the shuffled secrets dictionary
        self.reset()  #

    def reset(self) -> None:
        """
        Resets the game state to its initial state.
        :return: None
        """
        self.guesses = []
        self.secret_word_idx = (self.secret_word_idx + 1) % len(self.secrets_dictionary)
        self.secret_word = self.secrets_dictionary[self.order[self.secret_word_idx]]

    def guess(self, word: str) -> Tuple[str, Optional[str]]:
        """
        Takes in the next guess for the secret word and returns the scored guess.
        :param word: a string of the next guess for the secret word.
        :return: a tuple of the guess and a string of the same length as the guess that is scored according to the wordle algorithm.
         The second string is None if the guess is not valid, i.e. not found in the dictionary.
        """
        word = word.lower()
        if word not in self.full_dictionary:
            return word, None

        score = ['x'] * self.word_length  # initialize with fully wrong score

        # Counts how often each letter of the secret word appears in it
        secret_char_counter = Counter(self.secret_word)

        # Score fully correct letters
        for pos, (guess_char, sol_char) in enumerate(zip(word, self.secret_word)):
            if guess_char is sol_char:
                score[pos] = 'g'
                secret_char_counter[guess_char] -= 1

        # Score letters in the wrong position, that are still included
        for pos, (guess_char, sol_char) in enumerate(zip(word, self.secret_word)):
            if guess_char is not sol_char:
                if secret_char_counter.get(guess_char, 0) > 0:
                    score[pos] = 'y'
                    secret_char_counter[guess_char] -= 1

        score = ''.join(score)
        full_guess = (word, score)
        self.guesses.append(full_guess)
        return full_guess
