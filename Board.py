from game_types import Domino, Tail, Move
from typing import List

class Board(): 
    
    def __init__(self):
        self.board : list[Domino] = []

    def add_to_board(self, move: Move): 
        # Type control by defining Tail
        
        # Extracting information from input
        tile = move[0]
        tail = move[-1]

        # No repeating tiles
        if tile in self.board or (tile[-1], tile[0]) in self.board:
            raise TypeError("No repeating domino tiles allowed")

        # Ensuring order
        # If necessary, Domino pieces will be flipped to match the ends
        if self.is_empty():
            # Empty boards can have insertions as they come
            self.append_tile(tail, tile)
        else:
            # Check if any of the number on the tile match the chosen tail
            tail_number = self.get_tails(tail)
            if tail_number in tile:
                # The tile can be added to the board

                # Flipping if necessary
                if tile[tail] == tail_number:
                    # To add a tile to the tail (0), tile[-1] must be equal to the tail number
                    # To add a tile to the tail (-1), tile[0] must be equal to the tail number
                    # If the opposite is true, the domino tile must be flipped
                    tile = (tile[-1], tile[0])

                self.append_tile(tail, tile)
            else:
                # Invalid move
                raise TypeError("Invalid Move")



    def print_board(self): 
        print(f"------Domino Board--------")
        for tile in self.board:
            print(f"{tile}", end="")
        print()
    
    def get_board_tiles(self) -> list[Domino]: 
        return self.board
    
    def get_tails(self, tail : Tail | None = None) -> int | tuple[int, int]:
        # Get the tails of the board, or return empty list if none
        if self.is_empty():
            return []
        if tail == None:
            # Return both tails
            return (self.board[0][0], self.board[-1][-1])
        else:
            # Return specified tail
            return self.board[tail][tail]
    
    def append_tile(self, tail : Tail, tile : Domino):
        if tail == 0:
            # Append at the start
            self.board.insert(0, tile)
        else:
            # Append at the end
            self.board.append(tile)
    
    def is_empty(self) -> bool:
        return len(self.board) == 0
    

    def get_moves_for_tiles(self, domino: Domino) -> List[Move]:
        """
        Return list of legal moves for the given domino on this board.
        Each move is a tuple (tile, tail) where tail is 0 (left) or -1 (right).
        This implementation DOES NOT call get_tails() to avoid depending on its return type.
        """
        moves: List[Move] = []

        # Empty board: conventionally allow placing on the left (0)
        if self.is_empty():
            moves.append((domino, 0))
            return moves

        # Safely read the left and right end values directly from the board list
        # left_value = leftmost tile's left number
        # right_value = rightmost tile's right number
        left_value = self.board[0][0]
        right_value = self.board[-1][-1]

        a, b = domino

        # playable on left?
        if a == left_value or b == left_value:
            moves.append((domino, 0))

        # playable on right?
        if a == right_value or b == right_value:
            moves.append((domino, -1))

        return moves


    
    def copy(self):
        new_board = Board()
        # deep copy the tile list
        new_board.board = [tile for tile in self.board]  # creates a new list
        return new_board

# Testing Section   
if __name__ == "__main__":
    print("------------------------")
    print("Testing Board Class")
    board = Board()
    board.print_board()
    print(board.get_tails())
    board.add_to_board(((1,1), -1))
    board.print_board()
    board.add_to_board(((2,1), 0))
    board.print_board()
    board.add_to_board(((1,3), -1))
    board.print_board()
    board.add_to_board(((3,2), 0))
    board.print_board()
    board.add_to_board(((3,3), -1))
    board.print_board()
    print("------------------------")