# SPDX-FileCopyrightText: 2026 Lydia Winterscheidt  <lydia@example.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Exemplary test with pytest for completeness sake. Not fully formed, since this is not the focus of this exercise
import wordlegame
from util import read_file


def test_wordle_game():
    secrets_dictionary = read_file("data/wordle_easy.txt")
    full_dictionary = read_file("data/wordle_full.txt")
    test_game = wordlegame.WordleGame(secrets_dictionary, full_dictionary, 1)
    score = test_game.guess("paper")[1]
    assert score == "ggggg"
