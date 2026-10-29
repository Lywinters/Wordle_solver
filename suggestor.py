import time
from collections import Counter
import numpy as np
from string import ascii_lowercase

from util import read_file


class GreedySuggestor:
    def __init__(self):
        self._dictionary = read_file("data/wordle_full.txt")

        # dictionaries for translating between digits and chars
        self.translate = dict(zip(ascii_lowercase, range(26)))
        self.retranslate = dict(zip(range(26), ascii_lowercase))

        self._np_dictionary = np.array([[*([self.translate[char] for char in word])] for word in self._dictionary])
        word_amount, word_length = self._np_dictionary.shape
        self.dictionary_counts = np.zeros((word_amount, 26), dtype=np.byte)
        for col in range(word_length):
            self.dictionary_counts[np.arange(word_amount), self._np_dictionary[:, col]] += 1
        self._np_abridged = self._np_dictionary
        self.abridged_counts = self.dictionary_counts
        self.g_bonus = 0.2
        self.y_bonus = 1
        self.repeat_malus = 1

        self.used_letters = np.zeros(26, dtype=np.bool_)

    def suggest(self, hint):
        if hint is None:
            return ["aeros"]
        # Remove words from dictionary that can not be the solution anymore
        if hint is not None:
            valid_words = np.zeros(self._np_abridged.shape[0], dtype=np.bool_)
            missing = []
            count = {}
            for char, score in zip(*hint):
                self.used_letters[self.translate[char]] = 1
                if score == "x":
                    missing.append(char)
                else:
                    count[char] = count.get(char, 0) + 1
            for pos, word in enumerate(self._np_abridged):
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
                    if count_copy[word_char] < 0 and word_char in missing:
                        break
                else:
                    if all([val < 1 for val in count_copy.values()]):
                        valid_words[pos] = 1
            self._np_abridged = self._np_abridged[valid_words]
            self.abridged_counts = self.abridged_counts[valid_words]
        # score words
        score = np.zeros(self._np_dictionary.shape[0])
        score -= np.logical_and(self.dictionary_counts, self.used_letters).sum(axis=1) * self.repeat_malus * \
                 self._np_abridged.shape[0]
        score += np.equal(self._np_dictionary[:, np.newaxis], self._np_abridged[np.newaxis]).sum(
            axis=(1, 2)) * self.g_bonus
        score += np.minimum(self.dictionary_counts[:, np.newaxis], self.abridged_counts[np.newaxis]).sum(
            axis=(1, 2)) * self.y_bonus

        order = np.argsort(score)[::-1]
        best_scores = score[order[:5]]
        elements_new = self._np_dictionary[order[:5]]
        best_words = ["".join([self.retranslate[num] for num in word]) for word in elements_new]
        return best_words, best_scores

    def reset(self):
        self._np_abridged = self._np_dictionary
        self.abridged_counts = self.dictionary_counts
        self.used_letters = np.zeros(26)


if __name__ == '__main__':
    a = GreedySuggestor()

    while True:

        word = input("Guessed word: ")
        if word == "redo":
            a.reset()
            continue
        score = [*input("Score: ")]
        start = time.time()
        suggestion = a.suggest((word, score))
        print(f"Elapsed time: {time.time() - start}")
        print(suggestion[0])
        print(suggestion[1])
