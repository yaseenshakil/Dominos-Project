from Player import Player
from Board import Board 
from game_types import Domino, NUMBER_OF_TILES, ALL_TILES, Move
import math

class ExpectiMinimaxPlayer(Player): 
    """Expectiminimax Player

    Args:
        Player (Player): Inherits from the generic Player class
    """
    
    def __init__(self, name: str = "ExpectiMinimax", depth: int = 4):
        """Init Function for the Expectiminimax player

        Args:
            name (str, optional): _description_. Defaults to "ExpectiMinimax".
            depth (int, optional): Depth of search. Defaults to 4. !! HIGHER DEPTHS SLOW DOWN EXECUTION SIGNIFICANTLY!!
        """
        super().__init__(name)
        self.depth = depth

    def obtain_opponent_tile_probabilities(self, board: Board) -> list[tuple[Domino, float]]: 
        """Obtains the opponent tile probabilities based on the number of tiles that we have, number of tiles on the baord, and number of tiles in the boneyard. 

        Args:
            board (Board): takes the current state of the board as a parameter

        Returns:
            list[tuple[Domino, float]]: Returns a uniform probability distribution of each possible tile and the probability of the opponent having that tile
        """
        board_tiles = board.get_board_tiles()
        player_hand = self.get_hand()
        tiles_left = NUMBER_OF_TILES - (len(board_tiles) + len(player_hand))
        tile_probabilities = []
        # If there are no tiles left - end game scenario
        if tiles_left <= 0:
            return []
        # Iterate through all possible tiles
        for tile in ALL_TILES: 
            # If tile is not in the ExpectiMinimax player's hand nor on the observable board, add it to the tile_probabilities array 
            # with a probability of 1 / number of tiles left
            tile_flip = (tile[-1], tile[0])
            if (tile not in board_tiles and tile not in player_hand and tile_flip not in board_tiles and tile_flip not in player_hand): 
                tile_probabilities.append((tile, 1/tiles_left))
        return tile_probabilities
    
    def eval(self, board: Board, boneyard_size: int, hand: list[Domino]):
        """Evaluation function to capture score of the current game as it stands

        Args:
            board (Board): Current state of the board
            boneyard_size (int): number of tiles of the boneyard
            hand (list[Domino]): ExpectiMiniMax Player's hand

        Returns:
            int: Evaluation score
        """
        player_tiles = hand
        ## Metric #1: Number of tiles the opponent has compared to the number of tiles that the player has (Highest weighted metric) 
        opp_tile_count = NUMBER_OF_TILES - (boneyard_size + len(player_tiles) + len(board.get_board_tiles()))
        tile_count_score = (opp_tile_count - len(player_tiles))
        ## Metrix #2: Pip score captures the negative sum of the tile values in ExpectiMiniMax Player's hand. Lower tiles are preferable
        pip_score = -sum(a+b for (a,b) in player_tiles)
        ## Metric #3: Number of possible moves that the player can make. Flexibility is more valued. 
        mobility = len(self.possible_moves(board, player_tiles))
        return pip_score + 2*mobility + 5*tile_count_score

    def possible_moves(self, board: Board, hand: list[Domino] | None = None) -> list[Move]:
        """Obtains all the possible moves for the ExpectiMiniMax player specifically. 
        Captures the hypothetical possible moves given the state of a hand and board. 

        Args:
            board (Board): Current state of the bard
            hand (list[Domino] | None, optional): Current state of the hand. This is hypothetical during game simulation/search. Defaults to None.

        Returns:
            list[Move]: List of possible moves.
        """

        if hand is None:
            hand = self.get_hand()  
        moves = []
        tail_numbers = board.get_tails()

        for tile in hand:
            if board.is_empty() or tail_numbers[0] in tile:
                # Add move to tail if the tail number matches with tile
                moves.append((tile, 0))
            if not board.is_empty() and tail_numbers[-1] != tail_numbers[0] and tail_numbers[-1] in tile:
                # No need to add the move again if the tail numbers are the same
                # Or if the board is empty
                # Else, add move to tail if the tail number matches with tile
                moves.append((tile, -1))
        return moves

    
    def check_terminal(self, board: Board, hand, boneyard_size: int) -> bool:
        """Function evaluates whether we have reached a terminal state given the state of our 
        hand and the board

        Args:
            board (Board): Current state of the bard
            hand (list[Domino] | None, optional): Current state of the hand. This is hypothetical during game simulation/search. Defaults to None.
            boneyard_size: number of tiles in the boneyard

        Returns:
            bool: True if the state is terminal - one player has empty hands
        """
        if len(hand) == 0:
            # A state is terminal if the hand of the player is empty
            return True
        elif (NUMBER_OF_TILES - (len(hand) + boneyard_size + len(board.get_board_tiles()))) == 0:
            # A state is terminal if the hand of the opponent is empty
            return True
        else:
            return False


    def move(self, board: Board, boneyard_size: int) -> Move | None:
        """Move function for this player

        Args:
            board (Board): current state of the board
            boneyard_size (int): Number of tiles in the boneyard

        Returns:
            Move | None: Returns an optimal move
        """
        # Calls the max node (Player's search node) to obtain optimal move
        _, action = self.max_node(board, boneyard_size, depth=self.depth, hand=self.get_hand().copy())
        return action

    def max_node(self, board: Board, boneyard_size: int, depth: int, hand: list[Domino]):
        """Max Node is the node for the Expectiminimax player. It evaluates the best moves given a board, boneyard size, depth, and hand

        Args:
            board (Board): Current state of the board
            boneyard_size (int): Number of tiles in the boneyard 
            depth (int): Depth of search (Defaulted to 4)
            hand (list[Domino]): Current State of our hand

        Returns:
            Tuple(int, action): optimal value and move 
        """
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

    def chance_node(self, board: Board, boneyard_size: int, depth: int, hand: list[Domino]):
        """Chance node accounts for the probabilities of opponent tiles and for each possible tile, evaluates the score and 
        possible move for the opponent. Finally, it obtains a weightage of the minimum eval score multiplied by the tile probability

        Args:
            board (Board): Current State of the board
            boneyard_size (int): Number of boneyard tiles
            depth (int): depth of the search
            hand (list[Domino]): Current state of the hand after player plays the move

        Returns:
            total: int: Weighted score of the possible moves * probability of opponent having the tile
        """
        tile_probabilities = self.obtain_opponent_tile_probabilities(board)
        total = 0
        # tile_probabilities = [(Domino, probability), ...]
        for tile, prob in tile_probabilities:
            min_value = self.min_node(board, boneyard_size, depth, tile, hand)
            total += min_value * prob
        return total

    def min_node(self, board: Board, boneyard_size: int, depth: int, tile: Domino, hand: list[Domino]):
        """Min Node is the node for the opponent. It evaluates the best moves for opponent
          given a board, boneyard size, depth, and hand

        Args:
            board (Board): Current state of the board
            boneyard_size (int): Number of tiles in the boneyard 
            depth (int): Depth of search (Defaulted to 4)
            tile (Domino): Tile to be evaluated
            hand (list[Domino]): Current State of our hand

        Returns:
            Tuple(int, action): optimal value and move 
        """
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
