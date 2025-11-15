from Player import Player
from Board import Board
from game_types import Move

class HumanPlayer(Player):
    def __init__(self, name : str = "HumanPlayer"):
        super().__init__(name) 

    def move(self, board : Board, boneyard_size : int) -> Move | None:
        # A move made from a human player is based 
        # on observation of the current board and
        # choosing one of the possible moves
        moves = self.possible_moves(board)

        # If no possible move, return None
        if not moves:
            print("No possible moves")
            return None
        
        # Show Board
        board.print_board()

        # Show Hand
        print("Hand")
        print(self.get_hand())

        # Show possible moves
        for i in range(len(moves) - 1):
            print(f"Move #{i}: {moves[i]}", end=" | ")
        print(f"Move #{len(moves) - 1}: {moves[len(moves) - 1]}")
        
        # Choose move
        move_idx = -1
        while move_idx < 0 or move_idx >= len(moves):
            move_idx = int(input("Select a move by #: "))

        return moves[move_idx]