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
    
    

