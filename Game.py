
from Player import Player
from Board import Board
class Game(): 
    """
    Game Class to simulate game. Should contain function for possible actions for player, state, players hand, opponent players hand
    """

    ## Boilerplate initial function template
    def __init__(self, player: Player, opponent: Player, board: Board):
        self.player = player
        self.opponent = opponent
        self.board = board


    def is_terminal(self):
        return (self.player.get_hand() == [] or self.opponent.get_hand() == [])
    
    def get_possible_moves(self, player: Player):
        """Get Possible Moves for a player

        Args:
            player (Player Object): a player of type player is provided

        Returns:
            Array of possible moves: Returns an array of tuple (tile: tuple, index) i.e. tiles that player can play and on what end to play those tiles
        """
        result = []
        board_tiles = self.board.get_board_tiles()
        if (len(board_tiles) == 0): 
            result = [(tile, 0) for tile in player.get_hand()]
        else:
            tile_option = [board_tiles[0][0], board_tiles[-1][1]]
            for player_tile in player.get_hand():
                if (player_tile[0] == tile_option[0] or player_tile[1] == tile_option[0]): 
                    ## Add Tile to start of baord (left side) 
                    result.append((player_tile, 0))
                elif (player_tile[0] == tile_option[1] or player_tile[1] == tile_option[1]): 
                    ## Add Tile to end of board (right side)
                    result.append((player_tile, -1))
        return result
    
    def utility_score(self): 
        if (self.is_terminal()):
            sum = 0
            sum += self.sum_tiles(self.opponent)
            sum -= self.sum_tiles(self.player)

            return sum
        
    def sum_tiles(self, player: Player): 
        sum = 0
        for tile in player.get_hand():
            sum += tile[0] + tile[1]
        return sum
        
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
        
        









            
