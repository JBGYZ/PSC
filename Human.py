
from Board import Board, GameResult
from Player import Player


class Human(Player):
    """
    Allows the operator to play against the virtual agents
    """

    def __init__(self):
        """
        Nothing to do here apart from calling our super class
        """
        self.side = None
        super().__init__()

    def move(self, board: Board) -> (GameResult, bool):
        board.print_board()
        print("It's your turn to move ! Give a value in [0, 8]")
        action = int(input())
        _, res, finished = board.move(action, self.side)
        return res, finished

    def final_result(self, result: GameResult):
        if result.value == 1:
            show = "NAUGHT Wins !"
        elif result.value == 2:
            show = "CROSS Wins !"
        else:
            show = "It's a DRAW !"
        print(show)
        pass

    def new_game(self, side: int):
        self.side = side
        if side == 1:
            player = "NAUGHT"
        else:
            player = "CROSS"
        print("You are on the {} side !".format(player))
        pass

    def name(self):
        return "Human"

    def copy(self):
        pass
