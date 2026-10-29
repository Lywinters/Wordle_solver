from abc import ABC, abstractmethod

import numpy as np
from string import ascii_lowercase

class BaseSuggestor(ABC):
    def __init__(self, full_dictionary):
        self._dictionary = full_dictionary

    @abstractmethod
    def suggest(self, hint) -> list:
        """
        Essential functionality of the Suggestor classes. Suggests the next word to use based on some internal
        logic using the hint parameter.
        :param hint:
        :return:
        """
        pass


class GreedySuggestor(BaseSuggestor):
    """
    Simple Suggestor that scores all the words that could still be the secret word based on its parameters and
    returns a list of suggested next guesses sorted by the calculated score.
    The score is based on the expected quality of the potential guess when comparing it to all the remaining possible
    secret words.
    """
    def __init__(self, full_dictionary):
        super().__init__(full_dictionary)

        # dictionaries for translating between digits and chars, since working with
        self.translate = dict(zip(ascii_lowercase, range(26)))
        self.retranslate = dict(zip(range(26), ascii_lowercase))

        # translate word dictionary into numeric dictionary via the defined translations
        self._numeric_dictionary = np.array([[*([self.translate[char] for char in entry])] for entry in self._dictionary])
        word_amount, word_length = self._numeric_dictionary.shape

        # count how often each letter is present in the dictionary
        self.dictionary_counts = np.zeros((word_amount, 26), dtype=np.byte)
        for col in range(word_length):
            self.dictionary_counts[np.arange(word_amount), self._numeric_dictionary[:, col]] += 1

        # Favorite word to suggest as starting word
        self.favorite_starter = ["aeros"]


        # Parameters that are used for rating different possible guesses
        self.g_bonus = 0.2
        self.y_bonus = 1
        self.repeat_malus = 1

        # state variables that adapt to the guesses so far
        self.abridged_numeric_dictionary = None # numeric dictionary containing the remaining possible secret words
        self.abridged_dictionary_counts = None
        # array of length of the alphabet that keeps track of how often each letter is in the secret word
        self.used_letters = None

        self.reset()

    def reset(self):
        """
        Reset the Suggestor back to its initial state.
        :return: None
        """
        self.abridged_numeric_dictionary = self._numeric_dictionary
        self.abridged_dictionary_counts = self.dictionary_counts
        self.used_letters = np.zeros(26)

    def suggest(self, hint):
        """
        Generate a list of suggestions for next words to use in a game of wordle based on the information from the hints
        so far
        :param hint:
        :return:
        """
        # No guesses are made up to this point
        if hint is None:
            return self.favorite_starter

        # check which words could still be the secret word based on the hints
        valid_words = self._remove_incompatible_words(hint)
        self.abridged_numeric_dictionary = self.abridged_numeric_dictionary[valid_words]
        self.abridged_dictionary_counts = self.abridged_dictionary_counts[valid_words]

        # calculate the scores of the possible words based on the remaining secret words
        score = self._score_candidates()

        # sort the candidates based on scores and return the 5 best including their scores
        ranking = np.argsort(score,descending=True)
        best_scores = score[ranking[:5]]
        elements_new = self._numeric_dictionary[ranking[:5]]
        best_words = ["".join([self.retranslate[num] for num in word]) for word in elements_new]
        return best_words, best_scores

    def _score_candidates(self):
        """
        Scores the updated candidate based on the updated abridged list of remaining valid secret words.
        :return: the calculated score
        """
        score = np.zeros(self._numeric_dictionary.shape[0])
        # Deduct score for repeating letters to maximize information gain
        score -= np.logical_and(self.dictionary_counts, self.used_letters).sum(axis=1) * self.repeat_malus * \
                 self.abridged_numeric_dictionary.shape[0]
        # increase score for expected green letters in candidates
        score += np.equal(self._numeric_dictionary[:, np.newaxis], self.abridged_numeric_dictionary[np.newaxis]).sum(
            axis=(1, 2)) * self.g_bonus
        # increase score for expected yellow letters in candidates
        score += np.minimum(self.dictionary_counts[:, np.newaxis], self.abridged_dictionary_counts[np.newaxis]).sum(
            axis=(1, 2)) * self.y_bonus

        return score

    def _remove_incompatible_words(self,hint):
        """
        Removes incompatible words based on the ratings of the guesses from the dictionary to generate
        an abridged dictionary containing only valid guesses
        :param hint: a tuple of guess and score
        :return: a boolean array determining if an entry of the abridged dictionary is still valid
        """
        # Remove words from dictionary that cannot be the secret word anymore
        valid_words = np.zeros(self.abridged_numeric_dictionary.shape[0], dtype=np.bool_)
        absent_letters = []  # collect letters that are not in the secret word
        count = {}

        # Process "x" hints
        for char, score in zip(*hint):
            self.used_letters[self.translate[char]] = 1
            if score == "x":
                absent_letters.append(char)
            else:
                count[char] = count.get(char, 0) + 1
        for pos, word in enumerate(self.abridged_numeric_dictionary):
            count_copy = count.copy()
            for word_char, guess_char, guess_score in zip(word, *hint):
                word_char = self.retranslate[word_char]
                if guess_score == "g":
                    if word_char != guess_char:  # Invalid if different letter is in green position
                        break
                elif guess_score == "y":
                    if word_char == guess_char:  # Invalid if the same letter is in a yellow position
                        break
                count_copy[word_char] = count_copy.get(word_char, 0) - 1

                # Make sure that letters are not in the word too often.
                if count_copy[word_char] < 0 and word_char in absent_letters:
                    break
            else:
                if all([val < 1 for val in count_copy.values()]):
                    valid_words[pos] = 1

        return valid_words

