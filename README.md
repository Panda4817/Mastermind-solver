# Mastermind solver for Are You The One Show

I wanted to see if I could write a program that will find all 10 matches before the end of the show as the show is basically a game of mastermind i.e. the colours could be the males and the positions/numbers could be the females.

I tried model checking algorithm but due to a large number of variables that was too slow. With half the pairings the model checking does work well. So I used inference instead, using each episode's data to eliminate possible pairings.

## Requirements

Python 3
Data in a text file and input data from episodes

## Attribute

Thank you to CS50 AI course for the implementation of the model checking functions in logic.py.


