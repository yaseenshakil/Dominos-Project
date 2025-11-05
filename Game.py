
from Player import Player
class Game(): 
    """
    Game Class to simulate game. Should contain function for possible actions for player, state, players hand, opponent players hand
    """

    ## Boilerplate initial function template
    def __init__(self, player: Player, opponent: Player):
        self.player = player
        self.opponent = opponent
        self.players_hand = []
        self.opponents_hand = []
        self.board = [[(0,0)]]


    def is_terminal(self):
        return (self.players_hand == [] or self.opponents_hand == [])
    
    def utility_score(self): 
        if (self.is_terminal()):
            sum = 0
            sum += self.sum_tiles(self.player)
            sum -= self.sum_tiles(self.opponent)

            return sum
        
    def sum_tiles(self, player: Player): 
        sum = 0
        for tile in player.get_hand():
            sum += tile[0] + tile[1]
        return sum

    def get_possible_moves(self, player): 
        """Currently incomplete | get possible moves function

        Args:
            player (_type_): _description_

        Returns:
            Array of possible moves: Returns an array of moves i.e. tiles that player can play and on what end to play those tiles
        """
        return []
        
    def eval(self): 
        ## Possible considerations for evaluation function: Player having low numbered tiles combined with probabilistic guessing of opponent tiles, Checking number of possible player moves, Tile Count Difference between Player and Opponent, 
        ## Hand diversity | Pending work: Weight Determination, Probabilistic summing for opponents hand, possible late game tweaks to eval function
        w1,w2,w3 = 1,1,1
        score = 0
        ## Low Numbered Tile prioritization
        score += -self.sum_tiles(self.player)
        ## Board ends check to optimize playing options
        score += w2 * len(self.get_possible_moves(self.player))
        ## Tile Count Difference
        score += len(self.opponent.get_hand()) - len(self.player.get_hand())
        
        









            
