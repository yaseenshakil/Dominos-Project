from Player import Player
from Board import Board 
from game_types import Domino, NUMBER_OF_TILES, ALL_TILES, Move
import math

DEPTH = 4
class ExpectiMinimaxPlayer(Player): 
    
    def __init__(self, name: str = "ExpectiMinimax", depth: int = 4): 
        super().__init__(name)
        self.depth = depth

    # --- Opponent tile probabilities ---
    def obtain_opponent_tile_probabilities(self, board: Board) -> list[tuple[Domino, float]]: 
        board_tiles = board.get_board_tiles()
        player_hand = self.get_hand()
        tiles_left = NUMBER_OF_TILES - (len(board_tiles) + len(player_hand))
        tile_probabilities = []
        if tiles_left <= 0:
            return []
        for tile in ALL_TILES: 
            if (tile not in board_tiles and tile not in player_hand): 
                tile_probabilities.append((tile, 1/tiles_left))
        return tile_probabilities
    
    # --- Evaluation function ---
    def eval(self, board: Board, boneyard_size: int, hand: list[Domino]):
        """Evaluate board from the perspective of a simulated hand."""
        player_tiles = hand
        opp_tile_count = NUMBER_OF_TILES - (boneyard_size + len(player_tiles) + len(board.get_board_tiles()))
        pip_score = -sum(a+b for (a,b) in player_tiles)
        mobility = len(self.possible_moves(board, player_tiles))
        tile_count_score = (opp_tile_count - len(player_tiles))
        return pip_score + 2*mobility + 5*tile_count_score

    # --- possible_moves supports simulated hands ---
    def possible_moves(self, board: Board, hand: list[Domino] | None = None) -> list[Move]:
        if hand is None:
            hand = self.get_hand()  # default to real hand

        moves = []
        tail_numbers = board.get_tails()

        for tile in hand:
            tile_flip = (tile[-1], tile[0])
            # if (tile in board.get_board_tiles() or tile_flip in board.get_board_tiles()):
            #     continue
            if board.is_empty() or tail_numbers[0] in tile:
                moves.append((tile, 0))
            if not board.is_empty() and tail_numbers[-1] != tail_numbers[0] and tail_numbers[-1] in tile:
                moves.append((tile, -1))
        return moves
    
    def check_terminal(self, board: Board, hand, boneyard_size):
        if (NUMBER_OF_TILES - (len(board.get_board_tiles()) + len(hand) + boneyard_size) <= 0): return True
        return False 


    # --- Entry point ---
    def move(self, board: Board, boneyard_size: int) -> Move | None:
        value, action = self.max_node(board, boneyard_size, depth=self.depth, hand=self.get_hand().copy())
        return action

    # --- Max node ---
    def max_node(self, board: Board, boneyard_size: int, depth: int, hand: list[Domino]):
        if (depth == 0 or not hand or self.check_terminal(board, hand, boneyard_size)):
            return self.eval(board, boneyard_size, hand), None

        optimal_max_val = -math.inf
        optimal_max_move = None
        moves = self.possible_moves(board, hand)
        # Generate moves based on the current hand copy
        if not moves:
            return self.eval(board, boneyard_size, hand), None
        for action in moves:
            board_copy = board.copy()
            board_copy.add_to_board(action)

            # Simulate hand after playing this tile
            hand_copy = hand.copy()
            hand_copy.remove(action[0])

            value = self.chance_node(board_copy, boneyard_size, depth - 1, hand_copy)
            if value > optimal_max_val:
                optimal_max_val = value
                optimal_max_move = action

        return optimal_max_val, optimal_max_move

    # --- Chance node ---
    def chance_node(self, board: Board, boneyard_size: int, depth: int, hand: list[Domino]):
        tile_probabilities = self.obtain_opponent_tile_probabilities(board)
        total = 0
        for tile, prob in tile_probabilities:
            min_value = self.min_node(board, boneyard_size, depth, tile, hand)
            total += min_value * prob
        return total

    # --- Min node ---
    def min_node(self, board: Board, boneyard_size: int, depth: int, tile: Domino, hand: list[Domino]):
        if (depth == 0 or not hand or self.check_terminal(board, hand, boneyard_size)):
            return self.eval(board, boneyard_size, hand)

        opponent_moves = [
            m for m in board.get_moves_for_tiles(tile)
            if m[0] not in board.get_board_tiles() and (m[0][1], m[0][0]) not in board.get_board_tiles()
        ]
        if not opponent_moves:
            # Opponent passes, simulate next max turn
            return self.max_node(board, boneyard_size, depth - 1, hand)[0]

        worst_value = math.inf
        for action in opponent_moves:
            board_copy = board.copy()
            board_copy.add_to_board(action)
            value, _ = self.max_node(board_copy, boneyard_size, depth - 1, hand.copy())
            worst_value = min(worst_value, value)

        return worst_value
