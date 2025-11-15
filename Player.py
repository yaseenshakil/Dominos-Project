from game_types import Domino, Tail, Move
from Board import Board

class Player(): 
    """Class to describe the basic elements of any player/agent
    """
    def __init__(self): 
        self.hand : list[Domino] = []
        self.score : int = 0

    def get_hand(self) -> list[Domino]: 
        # Returns the player's hand
        return self.hand
    
    def set_hand(self, hand : list[Domino]):
        # Set a complete hand
        self.hand = hand

    def add_hand(self, tile : Domino):
        # Add a single tile to the hand
        self.hand.append(tile)
    
    def use_tile(self, tile : Domino):
        # Remove a tile from hand (making a move)
        if tile in self.hand:
            self.hand.remove(tile)
        elif (tile[-1], tile[0]) in self.hand:
            self.hand.remove((tile[-1], tile[0]))
        else:
            # The tile is not in hand
            raise TypeError("Tile not in hand")
    
    def possible_moves(self, board : Board) -> list[Move]:
        # A move is valid if at least one of the numbers in a tile,
        # match the tail numbers of the board
        # But if the board is empty, then any tile is valid
        
        moves = []

        tail_numbers = board.get_tails()

        for tile in self.hand:
            if board.is_empty() or tail_numbers[0] in tile:
                # Add move to tail if the tail number matches with tile
                moves.append((tile, 0))
            if not board.is_empty() and tail_numbers[-1] != tail_numbers[0] and tail_numbers[-1] in tile:
                # No need to add the move again if the tail numbers are the same
                # Or if the board is empty
                # Else, add move to tail if the tail number matches with tile
                moves.append((tile, -1))

        return moves

    def add_score(self, round_score : int):
        """ Add round score to the total score of the player
        """
        self.score += round_score
    
# Testing Section   
if __name__ == "__main__":
    print("------------------------")
    print("Testing Player Class")
    player = Player()
    board = Board()
    player.set_hand([(0, 2), (4, 5), (3, 4), (3, 6), (2, 3), (5, 6), (2, 5)])
    user = " "
    while len(player.possible_moves(board)) > 0:
        print("Hand")
        print(player.get_hand())
        print("Possible moves")
        moves = player.possible_moves(board)
        print(moves)
        user = input("Move #: ")
        if user == "":
            break
        board.add_to_board(moves[int(user)])
        player.use_tile(moves[int(user)][0])
        board.print_board()
    else:
        print("No more moves")
    print("Remaining hand")
    print(player.get_hand())
    print("------------------------")