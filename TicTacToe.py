
#
# Tic-Tac-Toe game
#

## Import

from Board import *
from Player import *
from toolkit import *
from time import time
import numpy as np
# import matplotlib.pyplot as plt

from RandomPlayer import *
from MinMaxAgent import *
from RndMinMaxAgent import *
from TQPlayer import *
from Human import *



## Random vs Random : benchmark

# battle(RandomPlayer(), RandomPlayer())
#
# # Same thing with a different function
# rumble([RandomPlayer()])



## Now with MinMax

# rumble([RandomPlayer(), MinMaxAgent(), RndMinMaxAgent()])



## Now with Tabular Q-learning (untrained)

# rumble([TQPlayer()])

# rumble([RandomPlayer(), MinMaxAgent(), RndMinMaxAgent(), TQPlayer()])



## Let's train various Tabular Q-learning players (as Player 2) and then test it against MinMax

### Against Random

# TrainedTQ_Random = TQPlayer()
#
# evolution_players(RandomPlayer(), TrainedTQ_Random)
# # Or
# evaluate_players(RandomPlayer(), TrainedTQ_Random)
# evolution_players(MinMaxAgent(), TrainedTQ_Random)



### Against MinMax

# TrainedTQ_MinMax = TQPlayer()
#
# evolution_players(MinMaxAgent(), TrainedTQ_MinMax)
# # Or
# evaluate_players(MinMaxAgent(), TrainedTQ_MinMax)
# evolution_players(MinMaxAgent(), TrainedTQ_MinMax)



### Against Random MinMax

# TrainedTQ_RndMinMax = TQPlayer()
#
# evolution_players(RndMinMaxAgent(), TrainedTQ_RndMinMax)
# # Or
# evaluate_players(RndMinMaxAgent(), TrainedTQ_RndMinMax)
# evolution_players(MinMaxAgent(), TrainedTQ_RndMinMax)



### Against itself

# TrainedTQ_self = TQPlayer()
# TrainedTQ_partner = TQPlayer()
#
# evolution_players(TrainedTQ_partner, TrainedTQ_self)
# TrainedTQ_self.export_TQ(file="TrainedTQ_self.txt")
# # Or
# evaluate_players(TrainedTQ_partner, TrainedTQ_self)
# evolution_players(MinMaxAgent(), TrainedTQ_self)



## Human player test

board = Board()
play_game(board, MinMaxAgent(), Human())




