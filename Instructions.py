
"""
Instructions for the Tic-Tac-Toe environment by Carsten Friedrich (Carsten.Friedrich@gmail.com)

There are 2 files needed : Board.py and Player.py
Fully execute those 2 files before importing them inside another file
"""

## Board.py

"""
Vocabulary :
Board = The 3x3 grid on which the game is played
Field = One of the 9 squares on the board. Can be EMPTY, NAUGHT or CROSS
Side = Either NAUGHT ('o') or CROSS ('x')
State = One of the 3^9 configurations of the board

Two classes in Board.py : GameResult and Board
"""

### GameResult

"""
Simply enumerates the 4 possibles categories of results for a certain state of the game : NOT_FINISHED, NAUGHT_WIN, CROSS_WIN, DRAW
"""

### Board

"""
state = A length 9 array representing the board

Includes many methods, of which only 4 are really useful

__init__ = Creates a new board. If a 9-array is given, will use it as the board
reset = Empties the board
move = Basically a `step` function. Updates the board when a move is played
other_side = Gives the value of the opposing player. Might be useful for coding inside a `Player`
"""

## Player.py

"""
One class inside : Player
"""

### Player

"""
Abstract class
When coding a new player, import this class and create a new class as such : `class NewPlayer(Player)`

4 methods :

__init__ = Don't forget to use `super().__init__()`
move = Usually uses the `move` from `Board` at the end
final_result = Allows the player to learn
new_game = Called before a game starts

Be careful to distinguish between `__init__` and `new_game` : if you `__init__` after every game, the player won't learn anything...
"""
