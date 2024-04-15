# takbot
This project is a minimax model with alpha-beta pruning for the boardgame of Tak. Currently, the game is not fully implemented, with the model only being able to place flat stones and move stacks by one tile.

Input files contain board states written in TPS format, explained [here](https://www.reddit.com/r/Tak/wiki/tak_positional_system)

The program can be run by directing the content of an input file to the input of the program, as follows:
```
python bot.py < tps/5x5-1.tps
```
