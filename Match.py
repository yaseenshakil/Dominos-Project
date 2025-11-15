from game_types import Domino, Tail, Move
from Boneyard import Boneyard
from Player import Player
from Board import Board

class Match(): 
    """Class to represent a match between two agents/players
    """

    """
    Match Class
        A match is a single round of the game, consisting of:
        1. A boneyard
        2. Random assignment of player hands until valid
        3. Taking moves in accordance to rules
        4. Determining winner of the match
        5. Score tracking

    """

    # Initialization of a match
    def __init__(self, player_1: Player, player_2: Player):
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = Board()
        self.boneyard = Boneyard()

        # Each player is dealt a hand
        self.player_1.set_hand(self.boneyard.generate_random_hand())
        self.player_2.set_hand(self.boneyard.generate_random_hand())

        # Repeat until hands are valid
        while not self.valid_hands():
            self.boneyard.restart_boneyard()
            self.player_1.set_hand(self.boneyard.generate_random_hand())
            self.player_2.set_hand(self.boneyard.generate_random_hand())

    def valid_hands(self) -> bool:
        """
        Check if hands (all players) are valid (no more than 5 doubles in a single hand)
        Doubles are same-sided tiles
        """
        return self.valid_hand(self.player_1) and self.valid_hand(self.player_2)
    
    def valid_hand(self, player : Player):
        """
        Check if the hand of a single player is valid
        """
        double_count = 0
        for tile in player.get_hand():
            if tile[0] == tile[-1]:
                # If double, add to count
                double_count += 1

        return double_count < 5
    
    def play(self):
        """Game Rules and executing the game
        """

        # The player with the highest double starts
        # If no player has a double, then the highest numbered
        # Tile goes first
        # Conversation is allowed to find out who is first

        # Order of domino tiles (which tile goes first)
        priority_order : list[Domino] = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 6)]
        
        # Ordering list according to priority rules
        priority_order.sort(key = lambda tile: (tile[0] + tile[-1]) + (100 if tile[0] == tile[-1] else 1), reverse=True)

        print(priority_order)




    
    

# Testing Section   
if __name__ == "__main__":
    print("------------------------")
    print("Testing Match Class")

    print("Initialization")
    p1 = Player()
    p2 = Player()
    m = Match(p1, p2)
    m.board.print_board()
    print("Boneyard")
    m.boneyard.print_boneyard_tiles()
    print(f"P1: {m.player_1.hand}")
    print(f"P2: {m.player_2.hand}")
    print()

    m.play()

    print("------------------------")