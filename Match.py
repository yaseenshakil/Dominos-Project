from Boneyard import Boneyard
from Player import Player
from Board import Board

class Match(): 
    """Class to represent a match between to agents/players
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
