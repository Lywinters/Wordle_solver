import random
from collections import Counter
from util import read_file


class Wordle:
    def __init__(self):
        self.dictionary = read_file("data/wordle_full.txt")
        self.answers = read_file("data/wordle_easy.txt")
        self.solution = None
        self.guesses = None
        self.word_length = len(self.dictionary[0])
        random.seed(1)
        self.order = list(range(len(self.answers)))
        self.pointer = -1
        random.shuffle(self.order)
        self.reset()

    def reset(self):
        self.guesses = []
        self.pointer = (self.pointer + 1) % len(self.answers)
        self.solution = self.answers[self.order[self.pointer]]
        # print(self.solution)

    def guess(self, word: str):
        word = word.lower()
        if word not in self.dictionary:
            return (word, None)
        correctness = ['x'] * self.word_length
        sol_counter = Counter(self.solution)
        for pos, (guess_char, sol_char) in enumerate(zip(word, self.solution)):
            if guess_char is sol_char:
                correctness[pos] = 'g'
                sol_counter[guess_char] -= 1

        for pos, (guess_char, sol_char) in enumerate(zip(word, self.solution)):
            if guess_char is not sol_char:
                if sol_counter.get(guess_char, 0) > 0:
                    correctness[pos] = 'y'
                    sol_counter[guess_char] -= 1
        full_guess = (word, correctness)
        self.guesses.append(full_guess)
        return full_guess
