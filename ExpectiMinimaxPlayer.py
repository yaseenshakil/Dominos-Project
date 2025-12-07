from Player import Player
from Board import Board 
from Game import Game
from game_types import Domino, NUMBER_OF_TILES, ALL_TILES, Move
import math



class ExpectiMinimaxPlayer(Player): 
    def __init__(self, name : str = "ExpectiMinimax"): 
        super().__init__(name)

    def obtain_opponent_tile_probabilities(self, board: Board) -> list[tuple[Domino, float]]: 
        board_tiles = board.get_board_tiles()
        player_hand = self.get_hand()
        tiles_left = NUMBER_OF_TILES - (len(board_tiles) + len(player_hand))
        tile_probabilities = []
        for tile in ALL_TILES: 
            if (tile not in board_tiles and tile not in player_hand): 
                tile_probabilities.append((tile, 1/tiles_left))
        return tile_probabilities
    
    def check_terminal(self, board: Board, boneyard_size: int) -> bool: 
        if (NUMBER_OF_TILES - (len(board.get_board_tiles()) + boneyard_size + len(self.get_hand())) == 0): 
            return True
        return False
    
    def eval(self, board: Board, boneyard_size: int):
        ## Evaluation function 
        player_tiles = self.get_hand()
        # You must store opponent tile count somewhere in Match; likely board or game state manages this
        opp_tile_count = NUMBER_OF_TILES - (boneyard_size + len(player_tiles) + len(board.get_board_tiles()))

        # 1. Reward lower pip sum
        pip_score = -sum(a+b for (a,b) in player_tiles)

        # 2. Reward legal moves (mobility)
        mobility = len(self.possible_moves(board))

        # 3. Reward having fewer tiles than opponent
        tile_count_score = (opp_tile_count - len(player_tiles))

        # Weighted sum
        return pip_score + 2*mobility + 5*tile_count_score

    def move(self, board : Board, boneyard_size : int) -> Move | None:
        value, action = self.max_node(board, boneyard_size, depth=3)
        return action
    
    def max_node(self, board: Board, boneyard_size: int, depth: int):
        # Check if depth is reached or a terminal stage is reached 
        if (depth == 0): 
            score = self.eval(board, boneyard_size)
            return score, None

        optimal_max_val = -math.inf
        optimal_max_move = None

        for action in self.possible_moves(board): 
            board_copy = board.copy()
            board_copy.add_to_board(action)

            value = self.chance_node(board_copy, boneyard_size, depth - 1)
            if value > optimal_max_val: 
                optimal_max_val = value
                optimal_max_move = action

        return optimal_max_val, optimal_max_move


    def chance_node(self, board: Board, boneyard_size: int, depth: int): 
        tile_probabilities = self.obtain_opponent_tile_probabilities(board)

        total = 0 
        for tile, prob in tile_probabilities: 
            min_value = self.min_node(board, boneyard_size, depth, tile)
            total += min_value * prob

        return total


    def min_node(self, board: Board, boneyard_size: int, depth: int, tile: Domino):

        opponent_moves = board.get_moves_for_tiles(tile)

        if not opponent_moves:
            # If opponent passes, you take another max turn
            return self.eval(board, boneyard_size)

        worst = math.inf

        for action in opponent_moves:
            board_copy = board.copy()
            board_copy.add_to_board(action)

            value, _ = self.max_node(board_copy, boneyard_size, depth - 1)
            worst = min(worst, value)

        return worst
