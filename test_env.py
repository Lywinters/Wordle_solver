import time

import wordle
import suggestor
from util import all_equal
import numpy as np

game = wordle.Wordle()
candidate = suggestor.GreedySuggestor()
wins = 0
total_guesses = np.zeros(len(game.answers) )
start = time.time()
for iterations in range(len(game.answers) ):
    word, score = game.guess("aeros")
    for guesses in range(1, 7):
        words, _ = candidate.suggest((word, score))
        word = words[0]
        _, score = game.guess(word)
        if score[0] == "g" and all_equal(score):
            wins += 1
            total_guesses[iterations] = guesses
            break
    game.reset()
    candidate.reset()
    if ((iterations + 1) % 100) == 0:
        print(f"Finished {iterations} out of {len(game.answers)} iterations in {time.time() - start} seconds.")
        print(f"{wins=} out of {iterations} rounds.")
        print(f"Average number of guesses was {total_guesses.sum() / wins:.2f}")
print(f"{wins=} out of {len(game.answers)} rounds.")
print(f"Average number of guesses was {total_guesses.sum() / wins:.2f}")
print([game.answers[wrongs] for wrongs in np.array(game.order)[total_guesses == 0]])
