## Wordle Game
Wordle is a well known word guessing game that got famous a few years back. 
The goal of the game is to guess a secret word using as few guesses as possible. The individual letters of each guess get scored and the player gets to know if the letter is in one of three categories:
- Not included in the secret word
- Included in the secret word but not in the position that was guessed
- Included in the secret word and also in the correct position.

The game can be played for example on [New York Times Games](https://www.nytimes.com/games/wordle/index.html).

## Wordle solver

The goal of this project is to provide a helpful tool for solving wordle games more efficiently. A simple heuristic suggester is included that accepts scored guesses as input and suggests what one should guess next.
The suggestions are made based on the included data sets of valid words to guess and the subset of those, called easy words, that could be the secret word.

## How to use

Executing the main.py file starts a command line program where the player inputs their guess and how the wordle game scored this guess. 
The algorithm will then propose the 5 candidates it thinks will be the best guesses for the next try.



## Installation
The code base uses python 3.12 and the packages mentioned in `requirements.txt`. To install them use.

```
pip install -r requirements.txt
´´´
