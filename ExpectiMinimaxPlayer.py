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

    def move(self, board : Board, boneyard_size : int) -> Move | None:
        value, action = self.max_node(board, boneyard_size, depth=3)
        return action
    
    def max_node(self, board: Board, boneyard_size: int, depth: int): 
        if (depth == 0 or self.check_terminal(board, boneyard_size)): 
            return 0, None
        optimal_max_val = -math.inf
        optimal_max_move = None

        for action in self.possible_moves(board): 
            board_copy = board.copy()
            board_copy.add_to_board(action)

            value, move = self.chance_node(board_copy, depth - 1)
            if (value > optimal_max_val): 
                optimal_max_val = value
                optimal_max_move= action
        return optimal_max_val, optimal_max_move


    def chance_node(self, board: Board, depth: int): 
        tile_probabilities = self.obtain_opponent_tile_probabilities(board)
        total = 0 
        for tile, prob in tile_probabilities: 
            min_value = self.min_node(board, tile, depth)
            total += min_value * prob
        return total

    def min_node(self, board: Board, tile: Domino, depth: int): 
        """Yet to implement

        Args:
            board (Board): _description_
            tile (Domino): _description_
            depth (int): _description_
        """
        return None

