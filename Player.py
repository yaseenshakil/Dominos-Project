from game_types import Domino, Tail, Move
from Board import Board

class Player(): 
    """Class to describe the basic elements of any player/agent
    """
    def __init__(self): 
        self.hand = []

    def get_hand(self) -> list[Domino]: 
        return self.hand
    
    def set_hand(self, hand : list[Domino]):
        self.hand = hand

    def add_hand(self, tile : Domino):
        self.hand.append(tile)
    
    def possible_moves(self, board : Board) -> list[Move]:
        # A move is valid if at least one of the numbers in a tile,
        # match the tail numbers of the board
        
        moves = []

        tail_numbers = board.get_tails()

        for tile in self.hand:
            if tail_numbers[0] in tile:
                # Add move to tail if the tail number matches with tile
                moves.append((tile, 0))
            if tail_numbers[-1] != tail_numbers[0] and tail_numbers[-1] in tile:
                # No need to add the move again if the tail numbers are the same
                # Else, add move to tail if the tail number matches with tile
                moves.append((tile, -1))

        return moves
    
