import time

from suggestor import GreedySuggestor
from util import read_file

if __name__ == '__main__':
    full_dictionary = read_file("data/wordle_full.txt")
    suggestor = GreedySuggestor(full_dictionary)

    while True:
        word = input("Guessed word: ")
        if word == "redo":
            suggestor.reset()
            continue
        score = [*input("Score: ")]
        start = time.time()
        suggestions = suggestor.suggest((word, score))
        print(f"Elapsed time: {time.time() - start}")
        print(suggestions[0])
        print(suggestions[1])