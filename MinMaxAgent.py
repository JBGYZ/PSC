#
# Copyright 2018 Carsten Friedrich (Carsten.Friedrich@gmail.com). All rights reserved
#

from Board import Board, EMPTY, GameResult
# Additional import might be needed, cf line 90
# from Board import BOARD_SIZE
from Player import Player


class MinMaxAgent(Player):
    """
    A computer player implementing the Min Max algorithm.
    This player behaves DETERMINISTICALLY.
    That is, for a given board position the player will always make the same move, even if other moves with the same evaluation exist.
    Already evaluated board positions are cached for efficiency.
    """

    WIN_VALUE = 1
    DRAW_VALUE = 0
    LOSS_VALUE = -1

    def __init__(self):
        """
        Getting ready for playing tic tac toe.
        """
        self.side = None
        """
        Cache to store the evaluation of board positions that we have already looked at.
        This avoids repeating a lot of work as we do not look at all the possible continuation from this position again.
        """
        self.cache = {}
        super().__init__()

    def new_game(self, side: int):
        """
        Setting the side for the game to come. Nothing else to do.
        :param side: The side this player will be playing
        """
        if self.side != side:
            self.side = side
            self.cache = {}

    def final_result(self, result: GameResult):
        """
        Does nothing.
        :param result: The result of the game that just finished
        :return:
        """
        pass

    # Internal function
    def _min(self, board: Board) -> (float, int):
        """
        Evaluate the board position `board` from the Minimizing player's point of view.
        :param board: The board position to evaluate
        :return: Tuple of (Best Result, Best Move in this situation). Returns -1 for best move if the game has already
        finished
        """

        #
        # First we check if we have seen this board position before, and if yes just return the cached value
        #
        board_hash = board.hash_value()
        if board_hash in self.cache:
            return self.cache[board_hash]

        #
        # Init the min value as well as action. Min value is set to DRAW as this value will pass through in case of a draw
        #
        min_value = self.DRAW_VALUE
        action = -1

        #
        # If the game has already finished we return. Otherwise we look at possible continuations
        #
        winner = board.who_won()
        # Depending on who won, we get the min value
        if winner == self.side:
            min_value = self.WIN_VALUE
            action = -1
        elif winner == board.other_side(self.side):
            min_value = self.LOSS_VALUE
            action = -1
        else:
            # Where are the empty spots, ie where can we play
            # *for index in [i for i, e in enumerate(board.state) if board.state[i] == EMPTY]:
            # -> This line of code is weird (for me) since `e` is neither used nor useful...
            # We can also use the following :
            # for index in [i for i in range(BOARD_SIZE) if board.state[i]==EMPTY]:
            # I chose to think he forgot to use `e`
            for index in [i for i, e in enumerate(board.state) if e == EMPTY]:
                b = Board(board.state)
                b.move(index, board.other_side(self.side))

                # Semi-recursion : we call `_max` on this hypothetical state
                res, _ = self._max(b)
                if res < min_value or action == -1:
                    min_value = res
                    action = index

                    # Shortcut: Can't get better than that, so abort here and return this move
                    # Explanation : if we get a `LOSS_VALUE` in one of the branches, then by taking `min(value_of_the_branches)`, we will necessarily get that `LOSS_VALUE`
                    if min_value == self.LOSS_VALUE:
                        self.cache[board_hash] = (min_value, action)
                        return min_value, action

                # Update the cache
                self.cache[board_hash] = (min_value, action)
        return min_value, action

    def _max(self, board: Board) -> (float, int):
        """
        Evaluate the board position `board` from the Maximizing player's point of view.
        :param board: The board position to evaluate
        :return: Tuple of (Best Result, Best Move in this situation). Returns -1 for best move if the game has already
        finished
        """

        #
        # First we check if we have seen this board position before, and if yes just return the cached value
        #
        board_hash = board.hash_value()
        if board_hash in self.cache:
            return self.cache[board_hash]

        #
        # Init the min value as well as action. Min value is set to DRAW as this value will pass through in case
        # of a draw
        #
        max_value = self.DRAW_VALUE
        action = -1

        #
        # If the game has already finished we return. Otherwise we look at possible continuations
        #
        winner = board.who_won()
        if winner == self.side:
            max_value = self.WIN_VALUE
            action = -1
        elif winner == board.other_side(self.side):
            max_value = self.LOSS_VALUE
            action = -1
        else:
            # cf the change in `_min`
            # for index in [i for i, e in enumerate(board.state) if board.state[i] == EMPTY]:
            for index in [i for i, e in enumerate(board.state) if e == EMPTY]:
                b = Board(board.state)
                b.move(index, self.side)

                # Semi-recursion
                res, _ = self._min(b)
                if res > max_value or action == -1:
                    max_value = res
                    action = index

                    # Shortcut: Can't get better than that, so abort here and return this move
                    if max_value == self.WIN_VALUE:
                        self.cache[board_hash] = (max_value, action)
                        return max_value, action

                # Update cache
                self.cache[board_hash] = (max_value, action)
        return max_value, action

    def move(self, board: Board) -> (GameResult, bool):
        """
        Making a move according to the MinMax algorithm
        :param board: The board to make a move on
        :return: The result of the move
        """
        # We take the maximizing player's point of view
        score, action = self._max(board)
        _, res, finished = board.move(action, self.side)
        return res, finished

    def name(self):
        return "MinMax"

    def copy(self):
        return MinMaxAgent()
